import random
import math
import pprint

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
    def __init__(self, nick, x=0, y=0, w=100,h=100):
        """
        The object constructor
        """
        self.cs=coordsys(x, w, y, h)
        self.width = w
        self.height = h
        self.name = nick
        
    def __str__(self):
        repr = "Room: %s W=%d H=%d" % (self.name, self.width, self.height)
        return repr
    
    def __repr__(self):
        repr = "{'room': '%s' 'W': '%d' 'H': '%d'}" % (self.name, self.width, self.height)
        return repr
            

if __name__ == "__main__":
    room1 = room("rm_nostalgia",w=300,h=100)
    room2 = room("rm_room1")
    ###make room = room[room_number] = room()
    lof_rooms = []
    for i in range(1,11):
        lof_rooms.append(room("rm_"+str(i),w=i*10,h=i*100/2))
    temp_input = input("Do you want to have the 2 example room appended to the lof_rooms? \n y/n")
    if temp_input == "y":
        lof_rooms.append(room1)
        lof_rooms.append(room2)
    print(*lof_rooms, sep="\n")
    pass

