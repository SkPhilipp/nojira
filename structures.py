class ScheduledLabel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


INDICATOR_LABEL = ScheduledLabel("+⚙️")
"""
Label to indicate an issue was created by this program.
"""


class ScheduledIssue:
    def __init__(self, number, name, content, label_names, board_name, milestone_name, state):
        self.number = number
        self.name = name
        self.content = content
        self.label_names = label_names
        self.board_name = board_name
        self.milestone_name = milestone_name
        self.state = state

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


class ScheduledMilestone:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
