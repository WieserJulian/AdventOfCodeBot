class Server:

    def __init__(self, id, channel, leader_api=""):
        self.id = id
        self.channel = channel
        self.leader_api = leader_api