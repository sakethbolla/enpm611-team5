import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

"""
This histogram visualizes how long it took to close GitHub issues tagged with the 'Type of Label like (kind/bug)' label. 
Each bar represents a time range (in days), showing how many issues were closed within that range. 
A red dashed line shows the average close time, and a contributor annotation box highlights who resolved the most issues for that label.
"""

def run(label=None):
    if not label:
        print("⚠️ Please provide a label using --label")
        return

    # Load data
    with open("data/poetry_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter issues by label
    filtered_issues = []
    for issue in data:
        labels = [lbl['name'] for lbl in issue.get("labels", [])]
        if label in labels:
            filtered_issues.append(issue)

    if not filtered_issues:
        print(f"❌ No issues found with label '{label}'")
        return

    # --- Metrics ---
    total_issues = len(filtered_issues)
    total_comments = sum(issue.get("comments", 0) for issue in filtered_issues)
    avg_comments = round(total_comments / total_issues, 2)

    time_to_close_days = []
    for issue in filtered_issues:
        if issue.get("closed_at"):
            created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
            closed = datetime.fromisoformat(issue["closed_at"].replace("Z", "+00:00"))
            duration = (closed - created).days
            time_to_close_days.append(duration)

    avg_close_time = round(sum(time_to_close_days) / len(time_to_close_days), 2) if time_to_close_days else "N/A"

    print(f"\n📌 Label-Based Insight for: '{label}'")
    print(f"• Total Issues: {total_issues}")
    print(f"• Average Comments: {avg_comments}")
    print(f"• Average Time to Close: {avg_close_time} days" if time_to_close_days else "• Average Time to Close: N/A")

    # --- Contributor Stats ---
    contributor_counter = {}
    for issue in filtered_issues:
        user = issue.get("user", {}).get("login")
        if user:
            contributor_counter[user] = contributor_counter.get(user, 0) + 1

    if contributor_counter:
        most_active_user = max(contributor_counter, key=contributor_counter.get)
        total_by_user = contributor_counter[most_active_user]
        resolved_by_user = sum(
            1 for issue in filtered_issues
            if issue.get("user", {}).get("login") == most_active_user and issue.get("closed_at")
        )
        total_contributors = len(contributor_counter)

        print(f"\n👥 Most Active Contributor for label '{label}':")
        print(f"• Number of issues created by top contributor: {total_by_user}")
        print(f"• Issues resolved (closed) by top contributor: {resolved_by_user}")
        print(f"• Total unique contributors: {total_contributors}")
        print(f"• Most Active Contributor: {most_active_user}")

    else:
        most_active_user = "N/A"

    # --- Visualization ---
    if time_to_close_days:
        avg_days = round(sum(time_to_close_days) / len(time_to_close_days), 2)

        plt.figure(figsize=(12, 6))
        counts, bins, patches = plt.hist(
            time_to_close_days,
            bins=10,
            edgecolor='black'
        )

        # Apply color gradient
        cmap = plt.get_cmap('plasma')
        for i, patch in enumerate(patches):
            patch.set_facecolor(cmap(i / len(patches)))

        # Add count labels
        for count, patch in zip(counts, patches):
            if patch.get_height() > 0:
                plt.text(
                    patch.get_x() + patch.get_width() / 2,
                    patch.get_height() + 0.5,
                    int(count),
                    ha='center',
                    fontsize=9,
                    fontweight='bold'
                )

        # Add average close time line
        plt.axvline(avg_days, color='red', linestyle='--', linewidth=2,
                    label=f'Avg Close Time = {avg_days} days')

        # Add top contributor annotation
        plt.annotate(
            f"Top Contributor: {most_active_user}\nResolved Issues: {resolved_by_user}",
            xy=(0.75, 0.93),
            xycoords='axes fraction',
            fontsize=10,
            ha='right',
            color='darkblue',
            bbox=dict(boxstyle="round,pad=0.3", fc="lavender", ec="gray", alpha=0.85)
        )

        # Legend
        plt.legend(loc='upper right', frameon=True, fancybox=True, shadow=True, fontsize=10)

        # Titles and formatting
        plt.title(f"🎯 Close Time Distribution for Label: '{label}'", fontsize=13, pad=20)
        plt.xlabel("Days to Close", fontsize=11)
        plt.ylabel("Number of Issues", fontsize=11)
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        plt.tight_layout()
        plt.show()
