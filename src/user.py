class User:

    def __init__(self, id: str, name: str,advent_of_code_name, reminder: bool):
        self.id = id
        self.name = name
        self.advent_of_code_name = advent_of_code_name
        self.reminder = reminder
