class ScheduledLabel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class ScheduledIssue:
    def __init__(self, number, name, content, labels):
        self.number = number
        self.name = name
        self.content = content
        self.labels = labels

    def __str__(self):
        return '{} - {}'.format(self.number, self.name)


class ScheduledProjectBoard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class ScheduledProjectBoardTask:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return '{} - {}'.format(self.name, self.content)


class ScheduledMilestone:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
