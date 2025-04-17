import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

def load_data(filepath):
    with open("data/poetry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

def analyze_contributors_and_reactions(data):
    creators = Counter()
    closers = Counter()
    reactions = defaultdict(int)

    for issue in data:
        creator = issue.get('user', {}).get('login')
        if creator:
            creators[creator] += 1

        closed_by = issue.get('closed_by')
        if closed_by and isinstance(closed_by, dict):
            closer = closed_by.get('login')
            if closer:
                closers[closer] += 1

        issue_reactions = issue.get('reactions', {})
        for reaction, count in issue_reactions.items():
            if reaction != 'url':
                reactions[reaction] += count

    return creators, closers, reactions

def plot_combined(creators, closers, reactions, top_n=10):
    top_creators = creators.most_common(top_n)
    top_closers = closers.most_common(top_n)
    reaction_items = sorted(reactions.items(), key=lambda x: x[1], reverse=True)

    fig, axs = plt.subplots(3, 1, figsize=(12, 15))

    # Top Creators
    users, counts = zip(*top_creators)
    axs[0].bar(users, counts)
    axs[0].set_title('Top Issue Creators')
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].set_ylabel('Created')

    # Top Closers
    users, counts = zip(*top_closers)
    axs[1].bar(users, counts, color='orange')
    axs[1].set_title('Top Issue Closers')
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].set_ylabel('Closed')

    # Reactions
    types, counts = zip(*reaction_items)
    axs[2].bar(types, counts, color='green')
    axs[2].set_title('Total Reactions on Issues')
    axs[2].tick_params(axis='x', rotation=45)
    axs[2].set_ylabel('Reactions')

    plt.tight_layout()
    plt.savefig('combined_issue_analysis.png')
    plt.show()

def main():
    data = load_data('data/poetry.json')  # Adjust path as needed
    creators, closers, reactions = analyze_contributors_and_reactions(data)

    print("\nTop Issue Creators:")
    for user, count in creators.most_common(10):
        print(f"{user}: {count}")

    print("\nTop Issue Closers:")
    for user, count in closers.most_common(10):
        print(f"{user}: {count}")

    print("\nReactions Summary:")
    for reaction, count in sorted(reactions.items(), key=lambda x: x[1], reverse=True):
        print(f"{reaction}: {count}")

    # Plot combined chart
    plot_combined(creators, closers, reactions)

if __name__ == '__main__':
    main()
