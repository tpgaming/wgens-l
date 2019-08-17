import random


class CoordinateSystem:
    class Cursor:
        def __init__(self, parent_coords, x, y):
            self.parent_coords = parent_coords
            self.x = x
            self.y = y

        def local_pos(self):
            return {'x': self.x, 'y': self.y}

        def global_pos(self):
            lp = self.local_pos()
            gp = self.parent_coords.global_pos()
            return {
                'x': gp['x'] + lp['x'],
                'y': gp['y'] + lp['y']
            }

    def __init__(self, minx, maxx, miny, maxy, parent=None):
        self.parent = parent
        self.nminx = minx
        self.nmaxx = maxx
        self.nminy = miny
        self.nminy = maxy

    def is_root(self):
        return self.parent is None

    def get_cursor(self):
        return CoordinateSystem.Cursor(self, 0, 0)


class Room:
    def __init__(self, world, nick, x=0, y=0, w=100, h=100):
        """
        The object constructor
        """
        self.world = world
        self.cs = CoordinateSystem(x, w, y, h, world.cs)
        self.width = w
        self.height = h
        self.name = nick
        self.x = x
        self.y = y

    def position(self):
        return {"x": self.x, "y": self.y}

    def __str__(self):
        obj_representation = "Room: %s W=%d H=%d" % (
            self.name, self.width, self.height
        )
        return obj_representation

    def __repr__(self):
        obj_representation = "{'Room': '%s' 'W': '%d' 'H': '%d'}" % (
            self.name, self.width, self.height
        )
        return obj_representation


class World:
    """
    World consists of one or  many rooms connected via portal
    tunnels. The global coordinates system is defined in World.
    World keeps track of the rooms and where they are placed in the
    World global coordinate system.
    """

    def __init__(self, xmin=0, xmax=1000, ymin=0, ymax=1000):
        # The global coordinate system
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        # Maximum Room size can be 30% of the current World
        self.max_room_size = 0.3
        # Free space management
        self.free = {
            "x_start": self.xmin, "y_start": self.ymin,
            "x_end": self.xmax, "y_end": self.ymax
        }
        self.cs = CoordinateSystem(self.xmin, self.xmax, self.ymin, self.ymax, parent=None)
        # The tracking of the rooms in the World, data model is
        # rooms = {
        #   "room1": room1_obj,
        #   ...
        #   "roomN": roomN_obj
        # }
        self.rooms = dict()
        # The portal tunnels we call simply sinks where game objects can sink to be
        # teleported from one end to another. It is guaranteed the both ends must be
        # connected to a Room.
        # Data model is
        # sinks = {
        #   "sink1": {
        #       "roomA": roomA_obj,
        #       "roomB": roomB_obj
        #   },
        #   ...
        #   "sinkN": {
        #       "roomAN": roomAN_obj,
        #       "roomBN": roomBN_obj
        #   }
        # }
        self.sinks = dict()

    def free_space(self):
        xfree = self.free['x_end'] - self.free['x_start']
        yfree = self.free['y_end'] - self.free['y_start']
        return (xfree > 0.05 * self.xmax) and (yfree > 0.05 * self.ymax)

    def create_room(self, nick):
        """
        Creates a new Room in the World and places it around to make sure
        the new Room does not overlap with the existing ones.
        Once done it registers the new Room in the database.
        """
        new_room = None
        # Generate the random position and size in the free space
        # The Room space allocation algorithm starts from 0,0 towards max x,y
        # Once a new Room is allocated the free space is updated, e.g.
        # self.free start values will be updated to prevent Room overlap in the World
        if self.free_space():
            x = random.randint(
                self.free['x_start'],
                self.free['x_start'] + self.free['x_end'] * 0.1)
            y = random.randint(
                self.free['y_start'],
                self.free['y_start'] + self.free['y_end'] * 0.1)
            # y = random.randint(self.free['y_start'], self.free['y_end'])
            x_size = random.randint(self.free['x_start'], self.free['x_end'])
            y_size = random.randint(self.free['y_start'], self.free['y_end'])
            # Normalize Room size to max. Room size allowed in this World
            if x_size > self.max_room_size * self.xmax:
                x_size = self.max_room_size * self.xmax
            if y_size > self.max_room_size * self.ymax:
                y_size = self.max_room_size * self.ymax
            # Verify if the Room fits into the free space available
            # If not normalize to fit
            xfree = self.free['x_end'] - self.free['x_start']
            if x_size > xfree:
                x_size = xfree
            yfree = self.free['y_end'] - self.free['y_start']
            if y_size > yfree:
                y_size = yfree
            new_room = Room(self, nick, x, x + x_size, y, y + y_size)
            # Register new Room
            self.rooms[nick] = new_room
            # Update free space
            self.free['x_start'] = self.free['x_start'] + x_size
            self.free['y_start'] = self.free['y_start'] + y_size
        return new_room


if __name__ == "__main__":
    game = World()
    room1 = game.create_room("rm_nostalgia")
    room2 = game.create_room("rm_room1")
    # make Room = Room[room_number] = Room()
    lof_rooms = []
    for i in range(1, 11):
        lof_rooms.append(game.create_room("rm_" + str(i)))  # ,w=i*10,h=i*100/2))
    # temp_input = input("Do you want to have the 2 example Room appended to the lof_rooms? \n y/n")
    # if temp_input == "y":
    #     lof_rooms.append(room1)
    #     lof_rooms.append(room2)
    print(*lof_rooms, sep="\n")
    pass
