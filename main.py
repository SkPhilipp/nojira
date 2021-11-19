#!/usr/bin/env python
import os

from indexer import Indexer

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

indexer = Indexer(GITHUB_TOKEN)
indexer.index('EffortGames/GameConcepts', '/designs')

print('\nlabels:')
for scheduled_label in indexer.scheduled_labels():
    print(scheduled_label)

print('\nissues:')
for scheduled_issue in indexer.scheduled_issues():
    print(scheduled_issue)

print('\nmilestones:')
for scheduled_milestone in indexer.scheduled_milestones():
    print(scheduled_milestone)

print('\nproject boards:')
for scheduled_project_board in indexer.scheduled_project_boards():
    print(scheduled_project_board)

print('\nproject board tasks:')
for scheduled_project_board_tasks in indexer.scheduled_project_board_tasks():
    print(scheduled_project_board_tasks)
