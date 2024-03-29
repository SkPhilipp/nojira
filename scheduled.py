import os
import re

from github import Github

from structures import *


class SchedulerConfig:
    def __init__(self,
                 override_board_name=None,
                 include_file_labels=True,
                 include_prefix=True):
        self.override_board_name = override_board_name
        self.include_file_labels = include_file_labels
        self.include_prefix = include_prefix


class SchedulerIndexedDocument:
    def __init__(self, repo_path, directory_path, file_name, content, config):
        self.repo_path = repo_path
        self.directory_path = directory_path
        self.file_name = file_name
        self.content = content
        self.config = config

    def labels(self):
        labels = [ScheduledLabel("v1"), INDICATOR_LABEL]
        # add directory as a label
        directory_name = os.path.basename(self.directory_path)
        labels.append(ScheduledLabel(directory_name))
        # remove extension from file_name, allow dots in filename
        file_name = os.path.basename(self.file_name)
        file_name = os.path.splitext(file_name)[0]
        # split file name by dots, interpret all as labels
        if self.config.include_file_labels:
            for label in file_name.split("."):
                labels.append(ScheduledLabel(label))
        return labels

    def _headers(self):
        # filter content on markdown '### ' headers
        headers = re.findall(r"^###\s(.*)$", self.content, re.MULTILINE)
        return headers

    def issues(self):
        issues = []
        # split file name by dots, interpret first as document name
        document_name = self.file_name.split(".")[0]
        # replace special characters in document name and directory name with spaces
        document_name = re.sub(r"[^\w\s]", " ", document_name)
        issue_prefix = f"{document_name.capitalize()}: " if self.config.include_prefix else ""
        board_name = self.project_board().name
        label_names = []
        for label in self.labels():
            label_names.append(label.name)
        milestone_name = None
        milestones = self.milestones()
        if len(milestones) == 1:
            milestone_name = milestones[0].name
        headers = sorted(self._headers())
        for header in headers:
            header_link = re.sub(r"[^\w]", "-", header).lower()
            issue_title = f"{issue_prefix}{header.capitalize()}"
            issue_body = f"See [{self.file_name}#{header_link}](https://github.com/{self.repo_path}/blob/master{self.directory_path}/{self.file_name}#{header_link})"
            issues.append(ScheduledIssue(None, issue_title, issue_body, label_names, board_name, milestone_name, "open"))
        return issues

    def milestones(self):
        milestones = []
        labels = self.labels()
        for label in labels:
            if re.match(r"v\d+", label.name):
                milestones.append(ScheduledMilestone(label.name))
        return milestones

    def project_board(self):
        board_name = self.config.override_board_name if self.config.override_board_name \
            else os.path.basename(self.directory_path).capitalize()
        return ScheduledProjectBoard(board_name)


class Scheduler:
    def __init__(self, token, config):
        self.client = Github(token)
        self.documents = []
        self.config = config

    def index(self, repo_path, directory_paths):
        repo = self.client.get_repo(repo_path)
        for directory_path in directory_paths:
            directory = repo.get_contents(directory_path)
            for file in directory:
                if file.name.endswith(".md"):
                    file_content = file.decoded_content.decode("utf-8")
                    document = SchedulerIndexedDocument(repo_path, directory_path, file.name, file_content, self.config)
                    self.documents.append(document)

    def labels(self):
        labels = set()
        for document in self.documents:
            labels.update(document.labels())
        return labels

    def issues(self):
        issues = set()
        for document in self.documents:
            issues.update(document.issues())
        return issues

    def milestones(self):
        milestones = set()
        for document in self.documents:
            milestones.update(document.milestones())
        return milestones

    def project_boards(self):
        project_boards = set()
        for document in self.documents:
            project_boards.update([document.project_board()])
        return project_boards
