import os
import re

from github import Github

from structures import *


class IndexedDirectory:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def scheduled_labels(self):
        labels = []
        directory_name = os.path.basename(self.directory_path)
        labels.append(ScheduledLabel(directory_name))
        return labels

    def scheduled_project_boards(self):
        boards = []
        directory_name = os.path.basename(self.directory_path)
        boards.append(ScheduledProjectBoard(directory_name))
        return boards


class IndexedDocument:
    def __init__(self, directory_path, file_name, content):
        self.directory_path = directory_path
        self.file_name = file_name
        self.content = content

    def scheduled_labels(self):
        labels = [ScheduledLabel('v1')]
        # remove extension from file_name, allow dots in filename
        file_name = os.path.basename(self.file_name)
        file_name = os.path.splitext(file_name)[0]
        # split file name by dots, interpret all as labels
        for label in file_name.split('.'):
            labels.append(ScheduledLabel(label))
        return labels

    def scheduled_issues(self):
        issues = []
        directory_name = os.path.basename(self.directory_path)
        # split file name by dots, interpret first as document name
        document_name = self.file_name.split()[0]
        issue_title = f"{directory_name} {document_name}"
        labels = self.scheduled_labels()
        issues.append(ScheduledIssue(None, issue_title, "Nondescript issue", labels))
        return issues

    def scheduled_milestones(self):
        milestones = []
        labels = self.scheduled_labels()
        for label in labels:
            if re.match(r'v\d+', label.name):
                milestones.append(ScheduledMilestone(label.name))
        return milestones

    def scheduled_project_board_tasks(self):
        tasks = []
        issues = self.scheduled_issues()
        for issue in issues:
            tasks.append(ScheduledProjectBoardTask(issue.name, issue.content))
        return tasks


class Indexer:
    def __init__(self, token):
        self.client = Github(token)
        self.directories = []
        self.documents = []

    def index(self, repo, directory_path):
        repo = self.client.get_repo(repo)
        directory = repo.get_contents(directory_path)
        indexed_directory = IndexedDirectory(directory_path)
        self.directories.append(indexed_directory)

        for file in directory:
            if file.name.endswith('.md'):
                file_content = file.decoded_content.decode('utf-8')
                indexed_file = IndexedDocument(directory_path, file.name, file_content)
                self.documents.append(indexed_file)

    def scheduled_labels(self):
        labels = []
        for directory in self.directories:
            labels.extend(directory.scheduled_labels())
        for document in self.documents:
            labels.extend(document.scheduled_labels())
        return labels

    def scheduled_issues(self):
        issues = []
        for document in self.documents:
            issues.extend(document.scheduled_issues())
        return issues

    def scheduled_milestones(self):
        milestones = []
        for document in self.documents:
            milestones.extend(document.scheduled_milestones())
        return milestones

    def scheduled_project_boards(self):
        project_boards = []
        for directory in self.directories:
            project_boards.extend(directory.scheduled_project_boards())
        return project_boards

    def scheduled_project_board_tasks(self):
        project_board_tasks = []
        for document in self.documents:
            project_board_tasks.extend(document.scheduled_project_board_tasks())
        return project_board_tasks
