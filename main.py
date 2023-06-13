import argparse
import csv
import datetime
import time

from github import Github

parser = argparse.ArgumentParser(description='Calculate Cycle Time, Time to Merge, and Size for pulls in a repository.')
parser.add_argument('-a', '--all', action="store_true", help="Write all closed PRs in the repo to csv.")
parser.add_argument('-d', '--date', help="Write pulls that were create after this date (YYYYMMDD).")
parser.add_argument('-s', '--sleep', help="Seconds to sleep after writing a row to the csv, don't exceed rate limits.")
args = parser.parse_args()

STOP_DATE = datetime.datetime.strptime(args.date, "%Y%m%d") if args.date is not None else None
SLEEP_SECONDS = int(args.sleep) if args.sleep is not None else 3

# Filter pull requests opened by the following users.
USERS_TO_TRACK = [
    "SOME_GITHUB_LOGIN_USER",
]

# Add api token here
GITHUB_API_TOKEN = "SOME_GITHUB_API_TOKEN"

# Add repo name here
REPO_NAME = "SOME_ORG/REPO_NAME"

g = Github(GITHUB_API_TOKEN)

repo = g.get_repo(REPO_NAME)

pulls = repo.get_pulls(state="closed", sort="created", direction="desc")

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
        "review speed (hours)",
        "url"
    ])

    for p in pulls:
        if STOP_DATE is not None and p.created_at < STOP_DATE:
            break

        user_login = p.user.login

        if args.all or user_login in USERS_TO_TRACK:
            pr_commits = p.get_commits()
            first_commit = pr_commits[0] if pr_commits.totalCount > 0 else None

            if first_commit is not None and p.merged_at is not None:
                first_commit_date = first_commit.commit.author.date
                total_diff_size = p.additions + p.deletions

                cycle_time = p.merged_at - first_commit.commit.author.date
                cycle_time_hours = cycle_time.days * 24 + cycle_time.seconds / 3600

                ttm = p.merged_at - p.created_at
                ttm_hours = ttm.days * 24 + ttm.seconds / 3600

                reviews = p.get_reviews()
                review_speed_hours = None
                if (reviews.totalCount > 0):
                    review_speed = reviews[0].submitted_at  - p.created_at
                    review_speed_hours = review_speed.days  * 24 + review_speed.seconds / 3600

                row = [
                    p.number,
                    p.title,
                    p.state,
                    total_diff_size,
                    user_login,
                    first_commit_date,
                    p.created_at,
                    p.merged_at,
                    round(ttm_hours, 2),
                    round(cycle_time_hours, 2),
                    round(review_speed_hours, 2) if review_speed_hours is not None else "",
                    p.html_url
                ]

                writer.writerow(row)
                print(row)
                time.sleep(SLEEP_SECONDS)  # Sleep to avoid exceeding github rate limit
