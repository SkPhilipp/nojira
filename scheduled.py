import os
import re

from github import Github

from structures import *


class SchedulerIndexedDocument:
    def __init__(self, directory_path, file_name, content):
        self.directory_path = directory_path
        self.file_name = file_name
        self.content = content

    def labels(self):
        labels = [ScheduledLabel("v1")]
        # add directory as a label
        directory_name = os.path.basename(self.directory_path)
        labels.append(ScheduledLabel(directory_name))
        # remove extension from file_name, allow dots in filename
        file_name = os.path.basename(self.file_name)
        file_name = os.path.splitext(file_name)[0]
        # split file name by dots, interpret all as labels
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
        issue_prefix = f"{document_name.capitalize()}"
        board_name = os.path.basename(self.directory_path).capitalize()
        labels = self.labels()
        headers = sorted(self._headers())
        for header in headers:
            issue_title = f"{issue_prefix}: {header.capitalize()}"
            issues.append(ScheduledIssue(None, issue_title, "Nondescript issue", labels, board_name))
        return issues

    def milestones(self):
        milestones = []
        labels = self.labels()
        for label in labels:
            if re.match(r"v\d+", label.name):
                milestones.append(ScheduledMilestone(label.name))
        return milestones

    def project_boards(self):
        boards = []
        board_name = os.path.basename(self.directory_path).capitalize()
        boards.append(ScheduledProjectBoard(board_name))
        return boards


class Scheduler:
    def __init__(self, token):
        self.client = Github(token)
        self.documents = []

    def index(self, repo_path, directory_path):
        repo = self.client.get_repo(repo_path)
        directory = repo.get_contents(directory_path)
        for file in directory:
            if file.name.endswith(".md"):
                file_content = file.decoded_content.decode("utf-8")
                document = SchedulerIndexedDocument(directory_path, file.name, file_content)
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
            project_boards.update(document.project_boards())
        return project_boards