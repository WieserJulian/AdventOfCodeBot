class Message:

    def __init__(self, id, message):
        self.id = id #YYYYDD
        self.message = message

    def __str__(self):
        return self.message.split("<field>")

    def __len__(self):
        return len(self.__str__())