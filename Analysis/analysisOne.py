import json
from collections import defaultdict
import matplotlib.pyplot as plt

# Load the JSON data
with open('/mnt/data/poetry_data.json', 'r', encoding='utf-8') as f:
    issues = json.load(f)

# Counters for issue creators and issue closers
created_by_counter = defaultdict(int)
closed_by_counter = defaultdict(int)

# Count issues created and closed by each user
for issue in issues:
    if 'user' in issue and issue['user'] and 'login' in issue['user']:
        created_by_counter[issue['user']['login']] += 1
    if 'closed_by' in issue and issue['closed_by'] and 'login' in issue['closed_by']:
        closed_by_counter[issue['closed_by']['login']] += 1

# Combine the counts for total activity (creation + closure)
combined_activity = defaultdict(int)
for user in set(list(created_by_counter.keys()) + list(closed_by_counter.keys())):
    combined_activity[user] = created_by_counter[user] + closed_by_counter[user]

# Get top 20 most active contributors
top_contributors = sorted(combined_activity.items(), key=lambda x: x[1], reverse=True)[:20]

# Prepare data for bar chart
users = [user for user, count in top_contributors]
counts = [count for user, count in top_contributors]

# Plotting the bar chart
plt.figure(figsize=(12, 6))
plt.barh(users[::-1], counts[::-1])
plt.xlabel('Total Issues Created + Closed')
plt.title('Top 20 Most Active Contributors')
plt.tight_layout()
plt.show()
