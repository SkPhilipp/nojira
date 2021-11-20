#!/usr/bin/env python
import os

from current import Loader
from scheduled import Scheduler
from synchronizer import Synchronizer

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = 'EffortGames/target-dummy'
scheduler = Scheduler(GITHUB_TOKEN)
scheduler.index(GITHUB_REPOSITORY, '/project')

loader = Loader(GITHUB_TOKEN)
loader.index(GITHUB_REPOSITORY)

synchronizer = Synchronizer(GITHUB_TOKEN, loader, scheduler)
synchronizer.print()
synchronizer.synchronize(GITHUB_REPOSITORY, dry_run=False)
