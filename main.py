#!/usr/bin/env python
import os

from scheduler import Scheduler

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

indexer = Scheduler(GITHUB_TOKEN)
indexer.index('EffortGames/GameConcepts', '/designs')

print('\n#### labels:')
for scheduled_label in indexer.labels():
    print(scheduled_label)

print('\n#### issues:')
for scheduled_issue in indexer.issues():
    print(scheduled_issue)

print('\n#### milestones:')
for scheduled_milestone in indexer.milestones():
    print(scheduled_milestone)

print('\n#### project boards:')
for scheduled_project_board in indexer.project_boards():
    print(scheduled_project_board)

print('\n#### project board tasks')
for scheduled_project_board_tasks in indexer.project_board_tasks():
    print(scheduled_project_board_tasks)
