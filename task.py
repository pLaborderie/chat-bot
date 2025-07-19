class Task:
    def __init__(self, name, description, is_completed=False, completed_message='Done', incomplete_message='To do'):
        self.name = name
        self.description = description
        self.is_completed = is_completed
        self.completed_message = completed_message
        self.incomplete_message = incomplete_message

    def status(self):
        return self.completed_message if self.is_completed else self.incomplete_message