from vector import Vector3
from mgr import Mgr
import random
from command import Target, Move2, Move
from unitAI import UnitAI

class GameMgr (Mgr):
    def __init__(self, engine):
        Mgr.__init__(self, engine)
        self.toggle = 0.15
        print "starting Game mgr"

        pass

    def loadLevel(self):
        self.game1()

    def releasLevel(self):
        for i in range(0,25):
            self.oblist.pop()
        pass

    def game1(self):
        self.ent1 = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes[0], pos = Vector3(-500, 2, -450))
        print "GameMgr Created: ", self.ent1.uiname, self.ent1.eid
        print "GameMgr Initializing aspects"
       
        self.ent2 = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes0[0], pos = Vector3(450, 2, 450), heading = 0)
        print "GameMgr Created: ", self.ent2.uiname, self.ent2.eid
        print "GameMgr Initializing aspects"

        self.oblist = []
        self.oblist2 = []
        self.engine.selectionMgr.addSelection(self.ent1)
        self.engine.selectionMgr.addSelection(self.ent2)

        x = [-1000,-1000]
        self.used = [(0,0)]
        for i in range(0,25):
            self.bord = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0], pos = Vector3( x[0], 2, x[1] ))
            self.oblist.append(self.bord)

            self.bord = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0], pos = Vector3( -1*x[0], 2, x[1] ))
            self.oblist.append(self.bord)

            self.bord = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0], pos = Vector3( x[1], 2, x[0] ))
            self.oblist.append(self.bord)

            self.bord = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0], pos = Vector3( x[1], 2, -1*x[0] ))
            self.oblist.append(self.bord)
	    
            x[1] += 80
        self.entbox = []
        x = [-900,900]
        test = False
        for h in range(0,random.randint(5,10)):
            i = random.randint(x[0], x[1])
            j = random.randint(x[0], x[1])
            for n,m in self.used:
                if n == i and m == j:
                    test = False
                else:                
                    i = random.randint(x[0], x[1])
                    j = random.randint(x[0], x[1])
            if test == True:
                self.box = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes2[0], pos = Vector3( i, 2, j))
                self.entbox.append(self.box)
                self.used.append((i,j))

        test = False
        for h in range(0,random.randint(5,10)):
            i = random.randint(x[0], x[1])
            j = random.randint(x[0], x[1])
            for n,m in self.used:
                if n == i and m == j:
                    test = False
                else:                
                    i = random.randint(x[0], x[1])
                    j = random.randint(x[0], x[1])
                    test = True
            if test == True:
                self.box = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes2[1],  pos = Vector3( i, 2, j))
                self.entbox.append(self.box)
                self.used.append((i,j))

        test = False
        for h in range(0,random.randint(5,10)):
            i = random.randint(x[0], x[1])
            j = random.randint(x[0], x[1])
            for n,m in self.used:
                if n == i and m == j:
                    test = False
                else:                
                    i = random.randint(x[0], x[1])
                    j = random.randint(x[0], x[1])
                    test = True
            if test == True:
                self.obs = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0],  pos = Vector3( i, 2, j))
                self.oblist.append(self.obs)
                self.used.append((i,j))

        test = False
        for h in range(0,random.randint(5,10)):
            i = random.randint(x[0], x[1])
            j = random.randint(x[0], x[1])
            for n,m in self.used:
                if n == i and m == j:
                    test = False
                else:                
                    i = random.randint(x[0], x[1])
                    j = random.randint(x[0], x[1])
                    test = True
            if test == True:
                self.obs = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes4[0], pos = Vector3( i, 2, j))
                self.oblist.append(self.obs)
                self.used.append((i,j))

        test = False
        for h in range(0,random.randint(5,10)):
            i = random.randint(x[0], x[1])
            j = random.randint(x[0], x[1])
            for n,m in self.used:
                if n == i and m == j:
                    test = False
                else:                
                    i = random.randint(x[0], x[1])
                    j = random.randint(x[0], x[1])
                    test = True
            if test == True:
                self.obs2 = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes7[0], pos = Vector3( i, 2, j))
                self.oblist2.append(self.obs2)
                self.used.append((i,j))

        self.rand = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes5[0], pos = Vector3( -900, 500, -900))


    def tick(self, dtime):
        
        for crash in self.entbox:
            if self.ent1.aspects[1].node._getWorldAABB().intersects(crash.aspects[1].node._getWorldAABB()):
                crash.pos *= -100000
                if (crash.uiname == 'BOX1') or (crash.uiname == 'BOX2') or (crash.uiname == 'BOX3'):
                    self.ent1.score += 100
                else: 
                    self.ent1.health -= 10
	
            if self.ent2.aspects[1].node._getWorldAABB().intersects(crash.aspects[1].node._getWorldAABB()):
                crash.pos *= -100000
                self.ent2.score += 100


        for crash2 in self.oblist:
            if self.ent1.aspects[1].node._getWorldAABB().intersects(crash2.aspects[1].node._getWorldAABB()):
                self.ent1.desiredSpeed *= -1.0

            if self.ent2.aspects[1].node._getWorldAABB().intersects(crash2.aspects[1].node._getWorldAABB()):
                self.ent2.desiredSpeed *= -1.0

	if (self.ent1.desiredSpeed < 0):
	    self.ent1.desiredSpeed += 1

	if (self.ent2.desiredSpeed < 0):
	    self.ent2.desiredSpeed += 1

        for crash3 in self.oblist2:
            if self.ent1.aspects[1].node._getWorldAABB().intersects(crash3.aspects[1].node._getWorldAABB()):
                crash3.pos *= -100000
                self.ent1.health -= 10

            if self.ent2.aspects[1].node._getWorldAABB().intersects(crash3.aspects[1].node._getWorldAABB()):
                crash3.pos *= -100000
                self.ent2.health -= 10

        if self.ent2.aspects[1].node._getWorldAABB().intersects(self.ent1.aspects[1].node._getWorldAABB()):
            self.ent1.desiredSpeed *= -0.5
            self.ent2.desiredSpeed *= -0.5

        # Shaky plane and creating boxes
#        if self.toggle >= 0: 
#            self.toggle -= dtime
        
#        if self.toggle < 0:
#            self.toggle = 0.105
        asp = self.rand.findAspect(UnitAI)
        asp.setCommand(Move(self.rand, Target(self.rand, Vector3(random.randint(-900,900), 500, random.randint(-900,900)))))


        if (random.randint(0,100) == 1):
            self.box = self.engine.entMgr.createEnt(self.engine.entMgr.entTypes2[random.randint(0,3)-1], pos = Vector3(self.rand.pos.x,500,self.rand.pos.z) ) #Vector3(self.rand.pos.x, 0, self.rand.pos.z))
            self.entbox.append(self.box)

	    #asp2 = self.box.findAspect(UnitAI)
            #asp2.setCommand(Move2(self.box, Target(None, Vector3(0,0,0))))
        for item in self.entbox:
            if item.pos.y > 5:
                item.vel.y -= item.deltaSpeed
                item.pos.y += item.vel.y
            if item.pos.y <= 0:
                item.vel.y = 0






