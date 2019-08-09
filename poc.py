import math
import pprint
import random
from os import PathLike


class coordsys:
    class cursor:
        def __init__(self, coordsys, x, y):
            self.coordsys = coordsys
            self.x = x
            self.y = y

        def local_pos(self):
            return {'x': self.x, 'y': self.y}


        def global_pos(self):
            lp = self.local_pos()
            gp = coordsys.global_pos()
            return {
                'x': gp['x']+lp['x'],
                'y': gp['y']+lp['y']
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
        return coordsys.cursor(self, 0, 0)

class room:
    def __init__(self, world, nick, x=0, y=0, w=100,h=100):
        """
        The object constructor
        """
        self.world = world
        self.cs=coordsys(x, w, y, h, world.cs)
        self.width = w
        self.height = h
        self.name = nick
        self.x = x
        self.y = y


    def position(self):
        return {"x": self.x, "y": self.y}


    def __str__(self):
        repr = "Room: %s W=%d H=%d" % (
                self.name, self.width, self.height
            )
        return repr


    def __repr__(self):
        repr = "{'room': '%s' 'W': '%d' 'H': '%d'}" % (
                self.name, self.width, self.height
            )
        return repr


class world:
    """
    World consists of one or  many rooms connected via portal
    tunnels. The global coordinates system is defined in world.
    World keeps track of the rooms and where they are placed in the
    world global coordinate system.
    """
    def __init__(self, xmin=0, xmax=1000, ymin=0, ymax=1000):
        # The global coordinate system
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        # Maximum room size can be 30% of the current world
        self.max_room_size = 0.3
        # Free space management
        self.free = {
            "x_start": self.xmin, "y_start": self.ymin,
            "x_end": self.xmax, "y_end": self.ymax
        }
        self.cs = coordsys(self.xmin, self.xmax, self.ymin, self.ymax, parent=None)
        # The tracking of the rooms in the world, data model is
        # rooms = {
        #   "room1": room1_obj,
        #   ...
        #   "roomN": roomN_obj
        #}
        self.rooms = dict()
        # The portal tunnels we call simply sinks where game objects can sink to be
        # teleported from one end to another. It is guaranteed the both ends must be
        # connected to a room.
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
        xfree = self.free['x_end']-self.free['x_start']
        yfree = self.free['y_end']-self.free['y_start']
        return (xfree > 0.05*self.xmax) and (yfree > 0.05*self.ymax)

    def create_room(self, nick):
        """
        Creates a new room in the world and places it around to make sure
        the new room does not overlap with the existing ones.
        Once done it registers the new room in the database.
        """
        new_room = None
        # Generate the random position and size in the free space
        # The room space allocation algorithm starts from 0,0 towards max x,y
        # Once a new room is allocated the free space is updated, e.g.
        # self.free start values will be updated to prevent room overlap in the world
        if self.free_space():
            x = random.randint(self.free['x_start'], self.free['x_end'])
            y = random.randint(self.free['y_start'], self.free['y_end'])
            x_size = random.randint(self.free['x_start'], self.free['x_end'])
            y_size = random.randint(self.free['y_start'], self.free['y_end'])
            # Normalize room size to max. room size allowed in this world
            if x_size > self.max_room_size*self.xmax:
                x_size = self.max_room_size*self.xmax
            if y_size > self.max_room_size*self.ymax:
                y_size = self.max_room_size*self.ymax
            # Verify if the room fits into the free space available
            # If not normalize to fit
            xfree = self.free['x_end']-self.free['x_start']
            if x_size > xfree:
                x_size = xfree
            yfree = self.free['y_end']-self.free['y_start']
            if y_size > yfree:
                y_size = yfree
            new_room = room(self, nick, x, x+x_size, y, y+y_size)
            # Register new room
            self.rooms[nick] = new_room
            # Update free space
            self.free['x_start'] = self.free['x_start']+x_size
            self.free['y_start'] = self.free['y_start']+y_size
        return new_room

if __name__ == "__main__":
    game = world()
    room1 = game.create_room("rm_nostalgia")
    room2 = game.create_room("rm_room1")
    ###make room = room[room_number] = room()
    lof_rooms = []
    for i in range(1,11):
        lof_rooms.append(room(game, "rm_"+str(i),w=i*10,h=i*100/2))
    # temp_input = input("Do you want to have the 2 example room appended to the lof_rooms? \n y/n")
    # if temp_input == "y":
    #     lof_rooms.append(room1)
    #     lof_rooms.append(room2)
    print(*lof_rooms, sep="\n")
    pass
