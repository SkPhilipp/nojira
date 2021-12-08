#!/usr/bin/env python
import os

from current import Loader
from scheduled import Scheduler
from synchronizer import Synchronizer


def nojira(repository_path, directory_path, dry_run):
    github_token = os.getenv('GITHUB_TOKEN', os.getenv('EG_GITHUB_TOKEN'))
    github_repository = os.getenv('GITHUB_REPOSITORY', repository_path)
    scheduler = Scheduler(github_token)
    scheduler.index(github_repository, directory_path)
    loader = Loader(github_token)
    loader.index(github_repository)
    synchronizer = Synchronizer(github_token, loader, scheduler)
    synchronizer.synchronize(github_repository, dry_run=dry_run)


nojira('EffortGames/GameConcepts', '/designs', dry_run=True)
nojira('EffortGames/TechnicalConcepts', '/designs', dry_run=True)
