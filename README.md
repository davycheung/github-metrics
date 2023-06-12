# GitHub Pull Metrics

[![License](https://img.shields.io/badge/License-MIT-blue)](https://en.wikipedia.org/wiki/MIT_License)

Python library to extract pulls from a github repository and calculate the following metrics on each pull: `Cycle Time`, `Time to Merge`, `Diff Size`

The data is written onto `pull_requests.csv` and is found in the script's directory.

## Install

```
pip install -r requirements.txt
```

## Setup

List the GitHub login users whose pulls we want to extract. 
```python
USERS_TO_TRACK = [
    "SOME_GITHUB_LOGIN_USER",
]
```

Add a GitHub token
```python
GITHUB_API_TOKEN = "github_pat_some_token"
```

Add a GitHub full repo name (including organization)
```python
REPO_NAME = "laravel/docs"
```

## Run Script

**Note: tested on python 3.8**

Only extract pulls for users specified in `USERS_TO_TRACK`:
```
python main.py
```

Extract pulls for all users:
```
python main.py -a
```

Extract pulls for all users that were created after 2023-Jun-01.
```
python main.py -a -d=20230601
```