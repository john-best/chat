class RPSGame:
    def __init__(self, room):
        self.player1 = room.get_owner();
        self.player2 = room.get_user();
        self.room = room
