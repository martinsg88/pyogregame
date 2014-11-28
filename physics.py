# Simple ORIENTED Physics for 38Engine
# vel is rate of change of pos
# Sushil Louis

from vector import Vector3
from aspect import Aspect
import utils
import math


class Physics (Aspect):
    def __init__(self, ent):
        Aspect.__init__(self, ent)
        pass 
        
    def tick(self, dtime):
        #----------position-----------------------------------
        timeScaledAcceleration = self.ent.acceleration * (dtime * 100)
        self.ent.speed += utils.clamp( self.ent.desiredSpeed - self.ent.speed, -timeScaledAcceleration, timeScaledAcceleration)

        #self.ent.vel.x = math.cos(-self.ent.heading) * self.ent.speed
        #self.ent.vel.z = math.sin(-self.ent.heading) * self.ent.speed
        #self.ent.vel.y = 0


        self.ent.vel = Vector3(self.ent.speed * math.cos(-self.ent.heading), 0, self.ent.speed * math.sin(-self.ent.heading))
        
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)

        #------------heading----------------------------------

        timeScaledRotation = self.ent.turningRate * (dtime*20)
        angleDiff = utils.diffAngle(self.ent.desiredHeading, self.ent.heading)
        dheading = utils.clamp(angleDiff, -timeScaledRotation, timeScaledRotation)
	print self.ent.desiredHeading
	print "meow"
	print self.ent.heading
        self.ent.heading += dheading
