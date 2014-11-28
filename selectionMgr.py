# Selection Manager tracks currently selected ent, selected group of ents, ...
import ogre.io.OIS as OIS

from mgr import Mgr


class SelectionMgr(Mgr):
    def __init__(self, engine):
        Mgr.__init__(self, engine)
        pass

    def initialize(self):
        pass
        # self.selectedEnts = []
        # self.toggle = 0
        # self.selectedEntIndex = 0
        # self.selectedEnt = self.engine.entMgr.ents[self.selectedEntIndex]


    def crosslink(self):
        self.keyboard = self.engine.inputMgr.keyboard


    def loadLevel(self):
        self.selectedEnts = []
        self.toggle = 0.1
        self.selectedEntIndex = 0
        self.selectedEnt = None #self.engine.entMgr.ents[self.selectedEntIndex]

    def tick(self, dtime):
        pass
    '''
        self.keyboard.capture()
 
        # Update the toggle timer.
        if self.toggle >= 0:
            self.toggle -= dtime

        # Check for TABKEY
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_TAB):
            # Update the toggle timer.
            self.toggle = 0.1

            if self.selectedEnt:
                self.selectedEnt.isSelected = False

            if self.selectedEntIndex >= len(self.engine.entMgr.ents) - 1:
                self.selectedEntIndex = 0 
            else: 
                self.selectedEntIndex = self.selectedEntIndex + 1

            self.selectedEnt = self.engine.entMgr.ents[self.selectedEntIndex]
            print "Selected Ent : ", self.selectedEnt.uiname
          
        if self.selectedEnt:
            self.selectedEnt.isSelected = True
    '''

    def addSelection(self, ent):
        self.engine.entMgr.ents[ent.eid].isSelected = True
        self.selectedEnts.append(ent)
        pass

    def setSelection(self, ent):
        self.clearSelection()
        self.engine.entMgr.ents[ent.eid].isSelected = True
        self.selectedEnts.append(ent)
        pass

    def clearSelection(self):
        for id, ent in self.engine.entMgr.ents.iteritems():
            ent.isSelected = False
        self.selectedEnts = []

    def primarySelection(self):
        if self.selectedEnts:
            return self.selectedEnts[0]
