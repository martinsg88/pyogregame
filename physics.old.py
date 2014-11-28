# Simple Physics for 38Engine
# vel is rate of change of pos
# Sushil Louis
import math

from aspect import Aspect
import ogre.renderer.OGRE as ogre
Vector3 = ogre.Vector3

class Physics(Aspect):
    def __init__(self, ent):
        Aspect.__init__(self, ent)
        self.ent.vel = Vector3(0, 0, 0)
        # sets self.ent
        
    def tick(self, dtime):
        '''update vel from ds, dh
        '''
        if self.ent.ds > self.ent.speed:
            self.ent.speed += self.ent.acceleration 
        elif self.ent.ds < self.ent.speed:
            self.ent.speed -= self.ent.acceleration 

        if self.ent.speed < 0:
            self.ent.speed = 0
        if self.ent.speed > self.ent.maxSpeed:
            self.ent.speed = self.ent.maxSpeed


        if self.ent.dh > self.ent.yaw:
            self.ent.nyaw = self.ent.yaw + (self.ent.turningRate * dtime)
        elif self.ent.dh < self.ent.yaw:
            self.ent.nyaw = self.ent.yaw - (self.ent.turningRate * dtime)

        x = self.ent.speed * math.sin(math.pi - self.ent.nyaw)
        z = self.ent.speed * math.cos(math.pi - self.ent.nyaw)
        
        self.ent.vel.x = -x
        self.ent.vel.y = 0
        self.ent.vel.z = z

        if self.ent.isSelected:
            print str(self.ent.vel)

        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)
        self.ent.deltaYaw = ogre.Radian(self.ent.nyaw - self.ent.yaw)
        self.ent.yaw = self.ent.nyaw

