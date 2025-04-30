import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import gzip

def analyze_contributors_and_reactions(data):
    """
    Processes the issue data to count:
    - Top issue creators
    - Top issue closers
    - Total reactions by type
    """
    creators = Counter()
    closers = Counter()
    reactions = defaultdict(int)

    for issue in data:
        # Count creators
        creator = issue.get('user', {}).get('login')
        if creator:
            creators[creator] += 1

        # Count closers
        closed_by = issue.get('closed_by')
        if closed_by and isinstance(closed_by, dict):
            closer = closed_by.get('login')
            if closer:
                closers[closer] += 1

        # Count reactions
        issue_reactions = issue.get('reactions', {})
        for reaction, count in issue_reactions.items():
            if reaction != 'url':
                reactions[reaction] += count

    return creators, closers, reactions

def plot_combined(creators, closers, reactions, top_n=10):
    """
    Creates a three-panel chart showing:
    - Top issue creators
    - Top issue closers
    - Total reaction counts
    """
    if not creators or not closers or not reactions:
        print("⚠️ No data to plot.")
        return
    top_creators = creators.most_common(top_n)
    top_closers = closers.most_common(top_n)
    reaction_items = sorted(reactions.items(), key=lambda x: x[1], reverse=True)

    fig, axs = plt.subplots(3, 1, figsize=(12, 14))  # Slightly smaller height

    # --- Top Creators ---
    users_c, counts_c = zip(*top_creators)
    axs[0].bar(users_c, counts_c, color='steelblue')
    axs[0].set_title('👤 Top Issue Creators', fontweight='bold')
    axs[0].set_ylabel('Issues Created', fontsize=11, fontweight='bold')
    axs[0].set_xlabel('User', fontsize=11, fontweight='bold')
    axs[0].tick_params(axis='x', labelrotation=60, labelsize=9)
    axs[0].set_xticklabels(users_c, ha='right', fontweight='bold')
    axs[0].tick_params(axis='y', labelsize=9)
    axs[0].yaxis.set_tick_params(labelsize=9)

    # --- Top Closers ---
    users_cl, counts_cl = zip(*top_closers)
    axs[1].bar(users_cl, counts_cl, color='coral')
    axs[1].set_title('🛠️ Top Issue Closers', fontweight='bold')
    axs[1].set_ylabel('Issues Closed', fontsize=11, fontweight='bold')
    axs[1].set_xlabel('User', fontsize=11, fontweight='bold')
    axs[1].tick_params(axis='x', labelrotation=60, labelsize=9)
    axs[1].set_xticklabels(users_cl, ha='right', fontweight='bold')
    axs[1].tick_params(axis='y', labelsize=9)
    axs[1].yaxis.set_tick_params(labelsize=9)

    # --- Reactions ---
    types_r, counts_r = zip(*reaction_items)
    axs[2].bar(types_r, counts_r, color='mediumseagreen')
    axs[2].set_title('🎉 Reactions Summary', fontweight='bold')
    axs[2].set_ylabel('Total Reactions', fontsize=11, fontweight='bold')
    axs[2].set_xlabel('Reaction Type', fontsize=11, fontweight='bold')
    axs[2].tick_params(axis='x', labelrotation=60, labelsize=9)
    axs[2].set_xticklabels(types_r, ha='right', fontweight='bold')
    axs[2].tick_params(axis='y', labelsize=9)
    axs[2].yaxis.set_tick_params(labelsize=9)

    plt.tight_layout(h_pad=2.5)
    plt.savefig('combined_issue_analysis.png')
    plt.show()


def run():
    """
    Entry point to load data, analyze contributors and reactions,
    print stats, and generate visualization.
    """
    """
    Loads JSON data from the specified file path.
    """
    with gzip.open("data/poetry_data.json.gz", "rt", encoding="utf-8") as f:
        data = json.load(f)

    creators, closers, reactions = analyze_contributors_and_reactions(data)

    print("\n📌 Top 10 Issue Creators:")
    for user, count in creators.most_common(10):
        print(f"• {user}: {count}")

    print("\n📌 Top 10 Issue Closers:")
    for user, count in closers.most_common(10):
        print(f"• {user}: {count}")

    print("\n📊 Reactions Summary:")
    for reaction, count in sorted(reactions.items(), key=lambda x: x[1], reverse=True):
        print(f"• {reaction}: {count}")

    # Show combined chart
    plot_combined(creators, closers, reactions)
