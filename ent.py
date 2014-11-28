# Entity class to hold information about entities for 381Engine, Spring2012
# Sushil Louis

from vector import Vector3
from physics import Physics
from renderable import Renderable
from control import Control1
from control import Control2
from wake import Wake
from unitAI import UnitAI

class Entity:
    #pos  = Vector3(0, 0, 0)
    #vel  = Vector3(0, 0, 0)

    def __init__(self, engine, eid, pos = Vector3(0,0,0), mesh = 'cigarette.mesh', vel = Vector3(0, 0, 0), heading = 0):
        self.engine = engine
        self.eid = eid
        self.pos = pos
        self.vel = vel
        self.mesh = mesh
        self.heading = heading
        self.speed = vel.length()
	self.score = 0
	self.health = 150

        self.length = 20
        self.width  = 5
        self.height = 15

        self.deltaSpeed = 5
        self.deltaYaw   = 0.01

        self.desiredSpeed = 0
        self.desiredHeading = 0
        #self.uiname = 'CIGARETTE'
        self.acceleration  = 6
        self.turningRate   = 0.1
        self.maxSpeed = 40

        self.wakeSize = 1


        self.isSelected = False
        self.aspects = []
        self.aspectTypes = [Physics, Renderable, Control1, Control2, Wake, UnitAI ]
    

        #----------------------------
        #self.initAspects()
        #----------------------------
        pass

    def initAspects(self):
        for aspectType in self.aspectTypes:
            self.aspects.append(aspectType(self))
        for aspect in self.aspects:
            aspect.initialize()

    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)

    def findAspect(self, aspType):
        for asp in self.aspects:
            if aspType == type(asp):
                return asp
        return None

    def __str__(self):
        x = "Entity: %s \nPos: %s, Vel: %s,  mesh = %s\nSpeed: %f, Heading: %f" % (self.uiname, str(self.pos), str(self.vel), self.mesh, self.speed, self.heading)
        return x

class ALIENSHIP(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'mfboat.mesh'
        self.uiname = 'mfboat'
        self.acceleration  = 100
        self.turningRate   = 0.3
        self.maxSpeed = 100
        
        self.wakeSize = 1
        self.length = 20
        self.width  = 5
        self.height = 15

class ALIENSHIP2(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'mfboat2.mesh'
        self.uiname = 'mfboat2'
        self.acceleration  = 100
        self.maxSpeed = 100
        
        self.wakeSize = 1
        self.length = 20
        self.width  = 5
        self.height = 15

class BOX1(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'box1.mesh'
        self.uiname = 'BOX1'
        self.wakeSize = 0



class BOX2(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'box2.mesh'
        self.uiname = 'BOX2'
        self.wakeSize = 0

class BOX3(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'box3.mesh'
        self.uiname = 'BOX3'
        self.wakeSize = 0

class BOMB1(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'bomb1.mesh'
        self.uiname = 'BOMB1'
        self.wakeSize = 0

class BUOY1(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'buoy1.mesh'
        self.uiname = 'BUOY1'

class RANDSHIP(Entity):
    def __init__(self, engine, eid, pos = Vector3(0,0,0), vel = Vector3(0, 0, 0), heading = 0):
        Entity.__init__(self, engine, eid, pos = pos, vel = vel, heading = heading)
        self.mesh = 'plane1.mesh'
        self.uiname = 'PLANE1'
        self.acceleration  = 100
        self.turningRate   = 0.3
        self.maxSpeed = 100
        
        self.wakeSize = 0
        self.length = 20
        self.width  = 5
        self.height = 15




