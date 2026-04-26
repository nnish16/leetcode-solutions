#!/usr/bin/env node

const fs = require('fs');

const LEETCODE_API_URL = 'https://leetcode.com/api/problems/all/';

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function slugToFilenamePart(slug) {
  return slug.replace(/-/g, '_');
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      'user-agent': 'leetcode-solutions-browser-executor/1.0',
      accept: 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  return response.json();
}

async function resolveProblemMeta(problemId, requestedSlug) {
  if (requestedSlug && !/^problem-\d+$/.test(requestedSlug)) {
    return { id: problemId, slug: requestedSlug, title: null };
  }

  const payload = await fetchJson(LEETCODE_API_URL);
  const stat = payload.stat_status_pairs.find(
    (entry) => Number(entry.stat.frontend_question_id) === Number(problemId),
  );
  if (!stat) {
    throw new Error(`Could not resolve LeetCode metadata for problem #${problemId}`);
  }
  return {
    id: problemId,
    slug: stat.stat.question__title_slug,
    title: stat.stat.question__title,
  };
}

class CdpPage {
  constructor(pageWebSocketUrl) {
    this.pageWebSocketUrl = pageWebSocketUrl;
    this.ws = null;
    this.nextId = 1;
    this.pending = new Map();
  }

  async connect() {
    await new Promise((resolve, reject) => {
      const ws = new WebSocket(this.pageWebSocketUrl);
      this.ws = ws;
      ws.onopen = () => resolve();
      ws.onerror = (error) => reject(error);
      ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (!msg.id) return;
        const pending = this.pending.get(msg.id);
        if (!pending) return;
        this.pending.delete(msg.id);
        if (msg.error) pending.reject(new Error(JSON.stringify(msg.error)));
        else pending.resolve(msg.result);
      };
      ws.onclose = () => {
        for (const [, pending] of this.pending.entries()) {
          pending.reject(new Error('CDP socket closed'));
        }
        this.pending.clear();
      };
    });
    await this.send('Page.enable');
    await this.send('Runtime.enable');
    await this.send('DOM.enable');
  }

  async close() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) this.ws.close();
  }

  async send(method, params = {}) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Timeout waiting for CDP method ${method}`));
      }, 20000);
      this.pending.set(id, {
        resolve: (value) => {
          clearTimeout(timeout);
          resolve(value);
        },
        reject: (error) => {
          clearTimeout(timeout);
          reject(error);
        },
      });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expression) {
    const result = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true,
      userGesture: true,
    });
    if (result.exceptionDetails) {
      throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text || 'Runtime.evaluate exception');
    }
    if (result.result?.subtype === 'error') {
      throw new Error(result.result.description || 'Runtime.evaluate error result');
    }
    return result.result ? result.result.value : undefined;
  }
}

let lastRun = null;

async function main() {
  const args = parseArgs(process.argv);
  const problemId = Number(args['problem-id']);
  const requestedSlug = args.slug || null;
  const solutionFile = args['solution-file'];
  const cdpUrl = args['cdp-url'] || 'http://127.0.0.1:56278';

  if (!Number.isInteger(problemId) || problemId <= 0) throw new Error('--problem-id is required');
  if (!solutionFile) throw new Error('--solution-file is required');

  const code = fs.readFileSync(solutionFile, 'utf8');
  const meta = await resolveProblemMeta(problemId, requestedSlug);
  const paddedId = String(problemId).padStart(4, '0');
  const expectedFileName = `${paddedId}_${slugToFilenamePart(meta.slug)}.py`;
  const targetUrl = `https://leetcode.com/problems/${meta.slug}/description/`;
  const cdpVersion = await fetchJson(`${cdpUrl}/json/version`);
  const pages = await fetchJson(`${cdpUrl}/json/list`);
  const preferredPage =
    pages.find((page) => page.type === 'page' && /leetcode\.com\/problems\//.test(page.url || '')) ||
    pages.find((page) => page.type === 'page');

  if (!preferredPage?.webSocketDebuggerUrl) throw new Error(`No attachable page found at ${cdpUrl}`);

  const run = {
    started_at: new Date().toISOString(),
    accepted: false,
    cdp: {
      http_url: cdpUrl,
      browser: cdpVersion.Browser,
      ws_url: cdpVersion.webSocketDebuggerUrl,
      attached_page_ws_url: preferredPage.webSocketDebuggerUrl,
      attached_page_url: preferredPage.url,
      attached_page_title: preferredPage.title,
    },
    problem: {
      id: problemId,
      slug: meta.slug,
      title: meta.title,
      target_url: targetUrl,
      expected_file_name: expectedFileName,
    },
    checkpoints: [],
  };

  lastRun = run;

  const page = new CdpPage(preferredPage.webSocketDebuggerUrl);
  await page.connect();
  const checkpoint = async (name, expression) => {
    const value = await page.eval(expression);
    run.checkpoints.push({ name, at: new Date().toISOString(), value });
    return value;
  };

  try {
    await checkpoint(
      'auth_verification_initial',
      `(() => ({
        href: location.href,
        title: document.title,
        signedIn: /Sign Out|My Lists|Settings|Nishant Sarang/.test(document.body.innerText),
        signInVisible: /Sign In/.test(document.body.innerText)
      }))()`,
    );

    await page.send('Page.navigate', { url: targetUrl });
    await sleep(5000);
    await checkpoint('after_navigation', `(() => ({ href: location.href, title: document.title, ready: document.readyState }))()`);
    await sleep(4000);

    const problemCheck = await checkpoint(
      'problem_detection',
      `(() => {
        const txt = document.body.innerText;
        return {
          href: location.href,
          title: document.title,
          body_has_expected_slug: location.href.includes(${JSON.stringify(`/${meta.slug}/`)}),
          body_has_problem_id: txt.includes(${JSON.stringify(`${problemId}. `)}),
          monaco_present: !!(globalThis.monaco && monaco.editor),
          models: (globalThis.monaco && monaco.editor) ? monaco.editor.getModels().map(m => ({ lang: m.getLanguageId(), len: m.getValueLength() })) : [],
          language_button: [...document.querySelectorAll('button')].map(b => b.innerText.trim()).find(t => /Python3|Python|C\\+\\+|Java|JavaScript|TypeScript/.test(t)) || null,
        };
      })()`,
    );

    const titleMatches = meta.title ? String(problemCheck?.title || '').includes(meta.title) : true;
    if (!problemCheck?.body_has_expected_slug || (!problemCheck?.body_has_problem_id && !titleMatches)) {
      throw new Error(`Failed to reach exact LeetCode problem page for #${problemId}`);
    }

    const languageResult = await checkpoint(
      'language_selection',
      `(() => {
        const textOf = (el) => (el && (el.innerText || el.textContent || '')).trim();
        const models = () => (globalThis.monaco && monaco.editor)
          ? monaco.editor.getModels().map((m) => ({ lang: m.getLanguageId(), len: m.getValueLength() }))
          : [];
        const allCandidates = [...document.querySelectorAll('button, [role="button"], [role="tab"], [role="option"], [role="menuitem"], div, span')];
        const currentLabels = allCandidates.map(textOf).filter(Boolean);
        const alreadyPython = models().some((m) => /python/i.test(m.lang || ''));
        if (alreadyPython) {
          return { selected: true, strategy: 'existing_python_model', models: models() };
        }

        const pythonDirect = allCandidates.find((el) => /^Python3?$/i.test(textOf(el)));
        if (pythonDirect) {
          pythonDirect.click();
          return { selected: true, strategy: 'direct_candidate', label: textOf(pythonDirect) };
        }

        const currentControl = allCandidates.find((el) => ['C++', 'Java', 'Python', 'Python3', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'Kotlin', 'Swift', 'Ruby', 'Scala', 'C#'].includes(textOf(el)));
        if (currentControl) {
          currentControl.click();
          return {
            selected: false,
            strategy: 'opened_picker_waiting_for_python',
            previous: textOf(currentControl),
            available: currentLabels.slice(0, 120),
          };
        }

        return {
          selected: false,
          strategy: 'language_control_not_found',
          available: currentLabels.slice(0, 120),
          models: models(),
        };
      })()`,
    );

    if (!languageResult?.selected) {
      for (let i = 0; i < 20; i += 1) {
        const retry = await page.eval(`(() => {
          const textOf = (el) => (el && (el.innerText || el.textContent || '')).trim();
          const candidates = [...document.querySelectorAll('button, [role="button"], [role="tab"], [role="option"], [role="menuitem"], div, span')];
          const pythonItem = candidates.find((el) => /^Python3?$/i.test(textOf(el)));
          if (pythonItem) {
            pythonItem.click();
            return { selected: true, label: textOf(pythonItem) };
          }
          const models = (globalThis.monaco && monaco.editor) ? monaco.editor.getModels().map((m) => ({ lang: m.getLanguageId(), len: m.getValueLength() })) : [];
          const alreadyPython = models.some((m) => /python/i.test(m.lang || ''));
          return { selected: alreadyPython, waiting: !alreadyPython, models, labels: candidates.map(textOf).filter(Boolean).slice(0, 120) };
        })()`);
        if (retry?.selected) {
          run.checkpoints.push({ name: 'language_selection_retry', at: new Date().toISOString(), value: retry });
          break;
        }
        await sleep(300);
        if (i === 19) {
          run.checkpoints.push({ name: 'language_selection_retry', at: new Date().toISOString(), value: retry });
        }
      }
    }

    await sleep(1200);

    const languageConfirmation = await checkpoint(
      'language_confirmation',
      `(() => {
        const textOf = (el) => (el && (el.innerText || el.textContent || '')).trim();
        const buttons = [...document.querySelectorAll('button')];
        const labels = buttons.map((b) => textOf(b)).filter(Boolean);
        const models = (globalThis.monaco && monaco.editor) ? monaco.editor.getModels().map((m) => ({ lang: m.getLanguageId(), len: m.getValueLength() })) : [];
        const pythonVisible = labels.some((label) => /^Python3?$/i.test(label));
        const pythonModel = models.some((m) => /python/i.test(m.lang || ''));
        return { pythonVisible, pythonModel, labels: labels.slice(0, 80), models };
      })()`,
    );

    if (!languageConfirmation?.pythonVisible && !languageConfirmation?.pythonModel) {
      throw new Error('Python was not confirmed on the page');
    }

    const beforePaste = await checkpoint(
      'editor_presence_before_paste',
      `(() => ({
        monaco_present: !!(globalThis.monaco && monaco.editor),
        models: (globalThis.monaco && monaco.editor) ? monaco.editor.getModels().map(m => ({ lang: m.getLanguageId(), len: m.getValueLength() })) : [],
        active_tag: document.activeElement && document.activeElement.tagName,
        active_classes: document.activeElement && document.activeElement.className,
      }))()`,
    );

    if (!beforePaste?.monaco_present) throw new Error('Monaco editor not detected');

    await page.eval(`(() => {
      const editorNode = document.querySelector('.monaco-editor');
      if (editorNode) editorNode.click();
      if (!(globalThis.monaco && monaco.editor)) return { applied: false, reason: 'monaco_missing' };
      const model = monaco.editor.getModels().find((m) => /python/i.test(m.getLanguageId())) || monaco.editor.getModels()[0];
      if (!model) return { applied: false, reason: 'model_missing' };
      model.setValue(${JSON.stringify(code)});
      return { applied: true, lang: model.getLanguageId(), len: model.getValueLength() };
    })()`);
    await sleep(1200);

    const afterPaste = await checkpoint(
      'editor_after_paste',
      `(() => {
        if (!(globalThis.monaco && monaco.editor)) return { applied: false, reason: 'monaco_missing' };
        const model = monaco.editor.getModels().find((m) => /python/i.test(m.getLanguageId())) || monaco.editor.getModels()[0];
        const value = model ? model.getValue() : '';
        const expected = ${JSON.stringify(code)};
        return {
          applied: !!model,
          lang: model ? model.getLanguageId() : null,
          len: value.length,
          first_line: value.split('\\n')[0] || null,
          matches_expected: value === expected,
          contains_class_solution: value.includes('class Solution'),
          contains_def: /def\\s+[A-Za-z_][A-Za-z0-9_]*\\s*\\(/.test(value),
        };
      })()`,
    );

    if (!afterPaste?.applied || !afterPaste?.matches_expected) {
      throw new Error('Editor model did not update with the intended Python solution');
    }

    const runClick = await checkpoint(
      'run_button_attempt',
      `(() => {
        const runButton = [...document.querySelectorAll('button')].find((b) => /^Run$/i.test(b.innerText.trim()));
        if (!runButton) return { available: false };
        runButton.click();
        return { available: true, clicked: true, text: runButton.innerText.trim() };
      })()`,
    );
    run.run_button = runClick;

    if (runClick?.available) {
      for (let i = 0; i < 45; i += 1) {
        const status = await page.eval(`(() => {
          const txt = document.body.innerText;
          return {
            accepted: /Accepted/.test(txt),
            wrong_answer: /Wrong Answer/.test(txt),
            runtime_error: /Runtime Error/.test(txt),
            compile_error: /Compile Error/.test(txt),
            time_limit: /Time Limit Exceeded/.test(txt),
            pending: /Running|Pending/.test(txt),
          };
        })()`);
        if (status.accepted || status.wrong_answer || status.runtime_error || status.compile_error || status.time_limit) {
          run.run_result = status;
          break;
        }
        await sleep(2000);
      }
      run.checkpoints.push({
        name: 'run_result_state',
        at: new Date().toISOString(),
        value: run.run_result || { unavailable: false, timeout: true },
      });
    } else {
      run.checkpoints.push({
        name: 'run_result_state',
        at: new Date().toISOString(),
        value: { unavailable: true, note: 'Run button not present on this LeetCode page state' },
      });
    }

    const submitClick = await checkpoint(
      'submit_button_attempt',
      `(() => {
        const submitButton = [...document.querySelectorAll('button')].find((b) => /^Submit$/i.test(b.innerText.trim()));
        if (!submitButton) return { available: false };
        submitButton.click();
        return { available: true, clicked: true, text: submitButton.innerText.trim() };
      })()`,
    );

    if (!submitClick?.available) throw new Error('Submit button was not available');

    let submitState = null;
    for (let i = 0; i < 60; i += 1) {
      submitState = await page.eval(`(() => {
        const txt = document.body.innerText;
        const idx = txt.indexOf('Test Result');
        return {
          href: location.href,
          title: document.title,
          accepted: /Accepted/.test(txt),
          wrong_answer: /Wrong Answer/.test(txt),
          runtime_error: /Runtime Error/.test(txt),
          compile_error: /Compile Error/.test(txt),
          time_limit: /Time Limit Exceeded/.test(txt),
          pending: /Submitting|Pending/.test(txt),
          testcase_passed: /testcases passed/.test(txt),
          all_submissions: /All Submissions/.test(txt),
          snippet: idx >= 0 ? txt.slice(Math.max(0, idx - 200), idx + 2200) : txt.slice(0, 2200),
        };
      })()`);
      const terminalAccepted = submitState.accepted && !submitState.pending && (
        String(submitState.href || '').includes('/submissions/') ||
        submitState.testcase_passed ||
        submitState.all_submissions
      );
      if (terminalAccepted || submitState.wrong_answer || submitState.runtime_error || submitState.compile_error || submitState.time_limit) break;
      await sleep(2000);
    }

    run.submit_result = submitState;
    run.checkpoints.push({ name: 'submit_result_state', at: new Date().toISOString(), value: submitState });

    run.accepted = Boolean(
      submitState?.accepted
      && ! submitState?.pending
      && (
        String(submitState.href || '').includes('/submissions/')
        || submitState?.testcase_passed
        || submitState?.all_submissions
      )
    );
    if (!run.accepted) throw new Error('Submission did not reach an Accepted state on the submissions page');

    run.finished_at = new Date().toISOString();
    process.stdout.write(`${JSON.stringify(run, null, 2)}\n`);
  } finally {
    await page.close();
  }
}

main().catch((error) => {
  const payload = lastRun || {};
  payload.accepted = false;
  payload.finished_at = new Date().toISOString();
  payload.error = { message: error.message, stack: error.stack };
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  process.exitCode = 1;
});
