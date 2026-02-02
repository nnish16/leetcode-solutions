import requests
import os
import json

# Configuration
REPO_PATH = "."  # Current folder
START_ID = 2     # Skip "Two Sum" if you want, or start at 1
DAILY_LIMIT = 5

def get_next_problems():
    # 1. Get official problem list (slugs)
    url = "https://leetcode.com/api/problems/all/"
    data = requests.get(url).json()
    
    # 2. Filter for free algorithms
    problems = []
    for p in data['stat_status_pairs']:
        if not p['paid_only']:
            problems.append({
                'id': p['stat']['question_id'],
                'title': p['stat']['question__title'],
                'slug': p['stat']['question__title_slug'],
                'difficulty': p['difficulty']['level'] # 1=Easy, 2=Med, 3=Hard
            })
            
    # 3. Sort by ID (1, 2, 3...)
    problems.sort(key=lambda x: x['id'])
    
    # 4. Find what we already solved (check filenames)
    existing_files = os.listdir(REPO_PATH)
    solved_ids = []
    for f in existing_files:
        if "_" in f:
            try:
                solved_ids.append(int(f.split("_")[0]))
            except:
                pass
                
    # 5. Pick next batch
    todo = []
    for p in problems:
        if p['id'] >= START_ID and p['id'] not in solved_ids:
            todo.append(p)
            if len(todo) >= DAILY_LIMIT:
                break
                
    return todo

if __name__ == "__main__":
    batch = get_next_problems()
    print("Here are your targets for today:")
    for p in batch:
        print(f"ID: {p['id']} | URL: https://leetcode.com/problems/{p['slug']}/")
