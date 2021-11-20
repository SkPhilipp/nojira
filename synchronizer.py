from random import random

from github import Github


class Synchronizer:
    def __init__(self, token, loader, scheduler):
        self.client = Github(token)
        # current entries
        self.current_labels = loader.labels()
        self.current_milestones = loader.milestones()
        self.current_issues = loader.issues()
        self.current_project_boards = loader.project_boards()
        # expected entries
        self.scheduled_labels = scheduler.labels()
        self.scheduled_milestones = scheduler.milestones()
        self.scheduled_issues = scheduler.issues()
        self.scheduled_project_boards = scheduler.project_boards()

    @staticmethod
    def _print_set(set_name, set_collection):
        if len(set_collection) > 0:
            print(f'{set_name}:')
            for item in set_collection:
                print(f'\t{item}')

    def print(self):
        print('\nSCHEDULED ENTRIES:\n')
        Synchronizer._print_set('scheduled labels', self.scheduled_labels)
        Synchronizer._print_set('scheduled milestones', self.scheduled_milestones)
        Synchronizer._print_set('scheduled issues', self.scheduled_issues)
        Synchronizer._print_set('scheduled project boards', self.scheduled_project_boards)
        print('\nCURRENT ENTRIES:\n')
        Synchronizer._print_set('current labels', self.current_labels)
        Synchronizer._print_set('current milestones', self.current_milestones)
        Synchronizer._print_set('current issues', self.current_issues)
        Synchronizer._print_set('current project boards', self.current_project_boards)

    def synchronize(self, repo_path, dry_run=False):
        print('\nSYNCHRONIZATION:\n')
        repo = self.client.get_repo(repo_path)
        # labels
        for scheduled_label in self.scheduled_labels:
            if scheduled_label not in self.current_labels:
                print(f'creating: label "{scheduled_label}"')
                if not dry_run:
                    random_color = ''.join([str(hex(int(random() * 16)))[-1] for _ in range(6)])
                    repo.create_label(name=scheduled_label.name, color=random_color)
            else:
                print(f'exists: label "{scheduled_label}"')
        # milestones
        for scheduled_milestone in self.scheduled_milestones:
            if scheduled_milestone not in self.current_milestones:
                print(f'creating: milestone "{scheduled_milestone}"')
                if not dry_run:
                    repo.create_milestone(title=scheduled_milestone.name)
            else:
                print(f'exists: milestone "{scheduled_milestone}"')
        # project boards
        for scheduled_project_board in self.scheduled_project_boards:
            if scheduled_project_board not in self.current_project_boards:
                print(f'creating: project board "{scheduled_project_board}"')
                if not dry_run:
                    repo.create_project(name=scheduled_project_board.name)
                    for project in repo.get_projects():
                        if project.name == scheduled_project_board.name:
                            project.create_column('Backlog')
                            project.create_column('To do')
                            project.create_column('In progress')
                            project.create_column('Done')
                            break
            else:
                print(f'exists: project board "{scheduled_project_board}"')
        # re-index labels
        labels_by_name = {}
        for label in repo.get_labels():
            labels_by_name[label.name] = label

        # re-index projects
        project_column_by_name = {}
        for project in repo.get_projects():
            project_columns = project.get_columns()
            for column in project_columns:
                if column.name == 'Backlog':
                    project_column_by_name[project.name] = column
                    break
        # issues & project board cards
        for scheduled_issue in self.scheduled_issues:
            if scheduled_issue not in self.current_issues:
                print(f'creating: issue "{scheduled_issue}"')
                if not dry_run:
                    mapped_labels = [labels_by_name[label.name] for label in scheduled_issue.labels]
                    created_issue = repo.create_issue(title=scheduled_issue.name, body=scheduled_issue.content, labels=mapped_labels)
                    project_column = project_column_by_name[scheduled_issue.board_name]
                    project_column.create_card(content_id=created_issue.id, content_type='Issue')
            else:
                print(f'exists: issue "{scheduled_issue}"')
