#!/usr/bin/env python
import os

from github import Github

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(GITHUB_TOKEN)

for repo in g.get_user().get_repos():
    print(repo.name)
