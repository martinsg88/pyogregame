from vector import Vector3
from mgr import Mgr



class EntMgr (Mgr):
    def __init__(self, engine):
        Mgr.__init__(self, engine)
        print "starting ent mgr"

        self.ents = {}
        self.nEnts = 0
        self.selectedEntIndex = 0
        self.selectedEnt = None
        self.selectedEnt2 = None
        import ent
        self.entTypes = [ent.ALIENSHIP]
	self.entTypes0 = [ent.ALIENSHIP2]
        self.entTypes2 = [ent.BOX1,ent.BOX2, ent.BOMB1]
        self.entTypes4 = [ent.BUOY1]
        self.entTypes5 = [ent.RANDSHIP]
        self.entTypes6 = [ent.BOX3]
        self.entTypes7 = [ent.BOMB1]
        

    def createEnt(self, entType, pos = Vector3(0,0,0), heading = 0):
        ent = entType(self.engine, self.nEnts, pos = pos, heading = heading)
        print "EntMgr created: ", ent.uiname, ent.eid, self.nEnts
        ent.initAspects()
        self.ents[self.nEnts] = ent;
        self.selectedEnt = ent
        self.selectedEntIndex = self.nEnts;
        self.nEnts = self.nEnts + 1
        return ent

    def selectNextEnt(self):
        self.selectedEnt = self.ents[0]
        self.selectedEnt2 = self.ents[1]
        print "EntMgr selected: ", str(self.selectedEnt)
        return self.selectedEnt

    def getSelected(self):
        return self.selectedEnt


    def tick(self, dt):
        for eid, ent in self.ents.iteritems():
            ent.tick(dt)
	pass

    def releaseLevel(self):
	#self.ents = []
        pass




