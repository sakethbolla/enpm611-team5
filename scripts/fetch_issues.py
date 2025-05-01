import requests
import json
import os
import gzip

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not set in environment variables.")

# GitHub personal access token
def load_config(config_path="../config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

# API endpoint
OWNER = config.get("OWNER")
REPO = config.get("REPO")
API_URL = f"https://api.github.com/repos/python-poetry/poetry/issues"

# Headers for authentication
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_issues():
    issues = []
    page = 1
    while True:
        print(f"Fetching issues page {page}...")
        response = requests.get(f"{API_URL}?state=all&per_page=100&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
    return issues

def fetch_issue_events(issue):
    events_url = issue.get("events_url")
    if not events_url:
        return []
    
    events = []
    page = 1
    while True:
        response = requests.get(f"{events_url}?per_page=100&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error fetching events for issue {issue.get('number')}: {response.status_code}")
            break
        data = response.json()
        if not data:
            break
        events.extend(data)
        page += 1
    return events

#function to fetch events 
def add_events_to_issues(issues):
    for issue in issues:
        print(f"Fetching events for issue #{issue.get('number')}...")
        issue['events'] = fetch_issue_events(issue)
    return issues


def save_issues_to_json(issues, file_path="../data/poetry_data.json.gz"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with gzip.open(file_path, "wt", encoding="utf-8") as f:
        json.dump(issues, f)
    print("Issues with events saved to", file_path)

if __name__ == "__main__":
    issues = fetch_issues()
    issues = add_events_to_issues(issues)
    save_issues_to_json(issues)
