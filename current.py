from github import Github

from structures import ScheduledLabel, ScheduledMilestone, ScheduledProjectBoard, ScheduledIssue


class Loader:
    def __init__(self, token):
        self.client = Github(token)
        self.indexed_labels = []
        self.indexed_issues = []
        self.indexed_milestones = []
        self.indexed_project_boards = []

    def index(self, repo):
        repo = self.client.get_repo(repo)
        repo.get_issues()
        for label in repo.get_labels():
            self.indexed_labels.append(ScheduledLabel(label.name))
        for milestone in repo.get_milestones():
            self.indexed_milestones.append(ScheduledMilestone(milestone.title))
        for issue in repo.get_issues(state="all"):
            issue_labels = []
            for label in issue.labels:
                issue_labels.append(label.name)
            milestone_name = issue.milestone.title if issue.milestone is not None else None
            self.indexed_issues.append(ScheduledIssue(issue.number, issue.title, issue.body, issue_labels, None, milestone_name, issue.state))
        for project_board in repo.get_projects():
            self.indexed_project_boards.append(ScheduledProjectBoard(project_board.name))

    def labels(self):
        return self.indexed_labels

    def issues(self):
        return self.indexed_issues

    def milestones(self):
        return self.indexed_milestones

    def project_boards(self):
        return self.indexed_project_boards
