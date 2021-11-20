class ScheduledLabel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class ScheduledIssue:
    def __init__(self, number, name, content, labels):
        self.number = number
        self.name = name
        self.content = content
        self.labels = labels

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class ScheduledProjectBoard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class ScheduledProjectBoardTask:
    def __init__(self, board, name, content):
        self.board = board
        self.name = name
        self.content = content

    def __str__(self):
        return f"{self.board} - {self.name}"

    def __eq__(self, other):
        return self.name == other.name and self.board == other.board

    def __hash__(self):
        return hash(self.name)


class ScheduledMilestone:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
