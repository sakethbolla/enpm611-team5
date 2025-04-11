import json
from collections import Counter
import matplotlib.pyplot as plt

# Function to load JSON data
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Function to analyze most active contributors
def analyze_most_active_contributors(data):
    issue_creators = Counter()
    issue_closers = Counter()

    for issue in data:
        # Count issue creators
        creator = issue.get('user', {}).get('login')
        if creator:
            issue_creators[creator] += 1

        # Count issue closers, with proper None check
        closed_by = issue.get('closed_by')
        if closed_by and isinstance(closed_by, dict):
            closer = closed_by.get('login')
            if closer:
                issue_closers[closer] += 1

    return issue_creators, issue_closers


# Function to plot top contributors
def plot_top_contributors(counter, title, filename, top_n=10):
    top_contributors = counter.most_common(top_n)
    users = [user for user, _ in top_contributors]
    counts = [count for _, count in top_contributors]

    plt.figure(figsize=(10, 6))
    plt.bar(users, counts)
    plt.title(title)
    plt.xlabel('User')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# Main function to run the analysis
def main():
    # Load data
    data = load_data('G:/poetry_data.json')

    # Analyze contributors
    issue_creators, issue_closers = analyze_most_active_contributors(data)

    # Print top creators and closers
    print("\nTop Issue Creators:")
    for user, count in issue_creators.most_common(10):
        print(f"{user}: {count} issues created")

    print("\nTop Issue Closers:")
    for user, count in issue_closers.most_common(10):
        print(f"{user}: {count} issues closed")

    # Plot results
    plot_top_contributors(issue_creators, 'Top Issue Creators', 'top_issue_creators.png')
    plot_top_contributors(issue_closers, 'Top Issue Closers', 'top_issue_closers.png')

if __name__ == '__main__':
    main()
