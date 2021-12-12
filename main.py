#!/usr/bin/env python
import os

from current import Loader
from scheduled import Scheduler, SchedulerConfig
from synchronizer import Synchronizer


def nojira(repository_path, directory_paths, dry_run, config=SchedulerConfig()):
    github_token = os.getenv('GITHUB_TOKEN', os.getenv('EG_GITHUB_TOKEN'))
    github_repository = os.getenv('GITHUB_REPOSITORY', repository_path)
    scheduler = Scheduler(github_token, config)
    scheduler.index(github_repository, directory_paths)
    loader = Loader(github_token)
    loader.index(github_repository)
    synchronizer = Synchronizer(github_token, loader, scheduler)
    synchronizer.synchronize(github_repository, dry_run=dry_run)


nojira('EffortGames/GameConcepts', ['/designs'],
       dry_run=True)
nojira('EffortGames/EffortGames', ['/Areas', '/Engine', '/Entities', '/Fuzzer',
                                   '/Items', '/Modifiers', '/Movement', '/Rollback',
                                   '/Scheduling', '/Serializer', '/Trading'],
       dry_run=True,
       config=SchedulerConfig(
           override_board_name="Engine",
           include_file_labels=False,
           include_prefix=False)
       )
