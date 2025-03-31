import requests
import json
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not set in environment variables.")

# GitHub personal access token
def load_config(config_path="/Users/bhavnakumari/ENPM_611_Team_5/team-5/enpm611-team5/config.json"):
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
        print(f"Fetching page {page}...")
        response = requests.get(f"{API_URL}?state=all&per_page=100&page={page}", headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        data = response.json()
        if not data:
            break
        issues.extend(data)
        page += 1
    return issues

def save_issues_to_json(issues, file_path="/Users/bhavnakumari/ENPM_611_Team_5/team-5/enpm611-team5/data/poetry_data.json"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=4)
    print("Issues saved to", file_path)

if __name__ == "__main__":
    issues = fetch_issues()
    save_issues_to_json(issues)