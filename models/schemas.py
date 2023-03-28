class Dialog:
    def __init__(self, args: tuple):
        self.id = args[0]
        self.text = args[1]
        self.next_dialog_id = args[2]

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()


class Choice:
    def __init__(self, args: tuple):
        self.id = args[2]
        self.choice = args[1]
        self.next_dialog_id = args[0]

    def __str__(self):
        return self.choice

    def __repr__(self):
        return self.__str__()


class Checkpoint:
    def __init__(self, args: tuple):
        self.id = args[0]
        self.yandex_user_id = args[1]
        self.dialog_checkpoint_id = args[2]

    def __str__(self):
        return f'Checkpoint<{self.id}>'

    def __repr__(self):
        return self.__str__()


class Achievement:
    def __init__(self, args: tuple):
        self.id = args[0]
        self.yandex_user_id = args[1]
        self.achievement = args[2]

    def __str__(self):
        return self.achievement

    def __repr__(self):
        return self.__str__()
