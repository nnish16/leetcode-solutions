class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in path.split('/'):
            if not part or part == '.':
                continue
            if part == '..':
                if stack:
                    stack.pop()
                continue
            stack.append(part)
        return '/' + '/'.join(stack)
