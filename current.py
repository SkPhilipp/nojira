from github import Github

from structures import ScheduledLabel, ScheduledMilestone, ScheduledProjectBoard, ScheduledIssue


class Loader:
    def __init__(self, token):
        self.client = Github(token)
        self.indexed_labels = set()
        self.indexed_issues = set()
        self.indexed_milestones = set()
        self.indexed_project_boards = set()

    def index(self, repo):
        repo = self.client.get_repo(repo)
        repo.get_issues()
        for label in repo.get_labels():
            self.indexed_labels.add(ScheduledLabel(label.name))
        for milestone in repo.get_milestones():
            self.indexed_milestones.add(ScheduledMilestone(milestone.title))
        for issue in repo.get_issues():
            issue_labels = []
            for label in issue.labels:
                issue_labels.append(label.name)
            self.indexed_issues.add(ScheduledIssue(issue.number, issue.title, issue.body, issue_labels, None))
        for project_board in repo.get_projects():
            self.indexed_project_boards.add(ScheduledProjectBoard(project_board.name))

    def labels(self):
        return self.indexed_labels

    def issues(self):
        return self.indexed_issues

    def milestones(self):
        return self.indexed_milestones

    def project_boards(self):
        return self.indexed_project_boards
