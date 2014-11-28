import ogre.renderer.OGRE as ogre
from aspect import Aspect
from vector import Vector3


MIN_SPEED = 2

class Wake(Aspect):

    def __init__(self, ent):
        Aspect.__init__(self, ent)
        pass

    def initialize(self):
        self.emitterList = [0,0,0]

        if self.ent.wakeSize == 0:
            self.wake = self.initWake(dimensions=(9,9), scalerRate=0.5, colorFaderAlpha=-0.5)
            self.midEmitter = Emitter(self.ent, ttl = 10, emissionRate = 2, position = (-self.ent.length+5, -0, 0))
            self.midEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.5), endColorAlpha = (1, 1, 1, 0.8))
        #set wake attributes based on boat size(1=small,2=med,3=large)
        if self.ent.wakeSize == 1:
            self.wake = self.initWake(dimensions=(12,18), scalerRate=0.5, colorFaderAlpha=-0.1)
            self.midEmitter = Emitter(self.ent, ttl = 10, emissionRate = 12, position = (-self.ent.length+5, -0, 0))
            self.midEmitter.setColorRange(startColorAlpha = (1, 1, 1, 0.5), endColorAlpha = (1, 1, 1, 0.8))

        else:
            print "No wakes for this type of entity", str(self.ent)

    def initWake(self, dimensions, scalerRate, colorFaderAlpha):
            self.ent.pSystem = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + str(self.ent.eid) + '_P')
            from renderable import Renderable
            self.wakeNode = self.ent.findAspect(Renderable).node.createChildSceneNode()
            self.wakeNode.attachObject(self.ent.pSystem)
            #self.ent.findAspect(Renderable).node.attachObject(self.ent.pSystem)
            
            #set up billboard so that particles face the right way
            self.renderer = self.ent.pSystem.getRenderer()
            self.renderer.setBillboardType(ogre.BBT_PERPENDICULAR_COMMON)
            self.renderer.setCommonDirection(ogre.Vector3(0,1,0))
            self.renderer.setCommonUpVector(ogre.Vector3(1,0,0))

            self.ent.pSystem.setMaterialName("Water/Wake")
            x, y = dimensions
            self.ent.pSystem.setDefaultDimensions(x, y)
            self.ent.pSystem.setParticleQuota(8000)

            #affectors
            self.scaler = self.ent.pSystem.addAffector("Scaler")
            self.colourFader = self.ent.pSystem.addAffector("ColourFader")   
            # #set up affector parameters          
            self.scaler.setParameter("rate", str(scalerRate))
            self.colourFader.setParameter("alpha", str(colorFaderAlpha))

    def getEmitters(self):
        #return (self.leftEmitter, self.midEmitter, self.rightEmitter)
        return (self.midEmitter,)

    def tick(self, dtime):

        if self.ent.speed < MIN_SPEED :
            self.ent.pSystem.setEmitting(False)
        else:
            self.ent.pSystem.setEmitting(True)

        for em in self.getEmitters():
            em.emitter.setParticleVelocity(1, 3) #self.ent.speed/2)
        
#------------------------------------------------------------------------------------------------------

class Emitter:
    '''An emitter with a configuration
    '''
    def __init__(self, ent, angle = ogre.Degree(8), ttl = 9, particleVelocity = (1, 3), emissionRate = 90, direction = Vector3(-1, 0, 0), position = Vector3(0, -10, 0)):
        self.ent = ent
        self.emitter = self.ent.pSystem.addEmitter("Point")
        self.emitter.setAngle(angle)
        self.emitter.setTimeToLive(ttl)
        low, high = particleVelocity
        self.emitter.setParticleVelocity(low, high)
        self.emitter.setDirection(direction)
        self.emitter.setEmissionRate(emissionRate)
	self.emitter.setPosition(position)


    def setColorRange(self, startColorAlpha = (1, 1, 1, 0.5), endColorAlpha = (1, 1, 1, 0.8)):
        self.emitter.setColourRangeStart(startColorAlpha)
        self.emitter.setColourRangeEnd(endColorAlpha)

