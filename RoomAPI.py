import json

class RoomHandler:
    def __init__(self):
        self.rooms = []
        self.next_id = 0

    def create_room(self, owner, password):
        new_room = Room(self.rooms, owner, self.next_id, password)
        self.rooms.append(new_room)
        self.next_id += 1
        return new_room

    def delete_room(self, room):
        if room in self.rooms:
            self.rooms.remove(room)
            return room
        return None

    def get_rooms(self):
        return self.rooms

    def get_room_ids(self):
        ids = []
        for room in self.rooms:
            ids.append(room.id)
        return ids

    def join_room(self, owner, guest):
        for room in self.rooms:
            if (room.owner == owner):
                room.join(guest)
                return

    def get_rooms_json(self):
        rooms_json_list = []
        for room in self.rooms:
            rooms_json_list.append(room.get_json())
        data = { "rooms": rooms_json_list }
        return data

    def get_room_json(self, room):
        for potential_room in self.rooms:
            if room is potential_room:
                return room.get_json()
        return None
    
    def room_check_exists(self, owner):
        for potential_room in self.rooms:
            if owner == potential_room.owner:
                return True
        return False

    def room_can_join(self, room, user, password=None):
        if room.owner == user or room.guest == user:
            if not room.has_password:
                return True
            else:
                # TODO: password check
                return True
        return False

    def get_room_by_owner(self, owner):
        for potential_room in self.rooms:
            if owner == potential_room.owner:
                return potential_room
        return None
    
    def get_room(self, id):
        for room in self.rooms:
            if id is room.id:
                return room
        return None

class Room:
    def __init__(self, rooms, owner, id, password):
        self.rooms = rooms
        self.owner = owner
        self.password = password
        self.guest = None
        self.id = id
        self.has_password = False

        if self.password is not '':
            self.has_password = True

    def join(self, guest):
        self.guest = guest

    def part(self, user):
        if user is self.owner:
            rooms.remove(self)
            return True
        if self.guest is user:
            self.guest = None
            return True
        return False
    
    def get_json(self):
        data = {
                'room': {
                    'id': '{}'.format(self.id),
                    'owner': '{}'.format(self.owner),
                    'guest': '{}'.format(self.guest),
                    'password': '{}'.format(str(self.has_password).lower()),
                    }
                }
        return data
