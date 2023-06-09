import csv
import os

from github import Github

g = Github(os.getenv('GITHUB_API_TOKEN'))
alloy_repo = g.get_repo(os.getenv('REPO_NAME'))

pulls = alloy_repo.get_pulls(state="closed")

with open('pull_requests.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        "number",
        "title",
        "state",
        "diff size",
        "user",
        "first commit",
        "created_at",
        "merged_at",
        "time to merge (hours)",
        "cycle time (hours)",
        "url"
    ])

    for p in pulls:
        pr_commits = p.get_commits()
        first_commit = pr_commits[0] if pr_commits.totalCount > 0 else None
        first_commit_date = first_commit.commit.author.date
        total_diff_size = p.additions + p.deletions

        if first_commit is not None and p.merged_at is not None:
            cycle_time = p.merged_at - first_commit.commit.author.date
            cycle_time_hours = cycle_time.days * 24 + cycle_time.seconds / 3600

            ttm = p.merged_at - p.created_at
            ttm_hours = ttm.days * 24 + ttm.seconds / 3600

            writer.writerow([
                p.number,
                p.title,
                p.state,
                total_diff_size,
                p.user.login,
                first_commit_date,
                p.created_at,
                p.merged_at,
                round(ttm_hours, 2) if p.merged_at is not None else "",
                round(cycle_time_hours, 2) if p.merged_at is not None else "",
                p.html_url
            ])
