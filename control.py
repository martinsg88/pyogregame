import ogre.io.OIS as OIS

from aspect import Aspect
import utils

class Control1(Aspect):
    def __init__(self, ent):
        Aspect.__init__(self, ent)

    def initialize(self):
        self.ent.desiredHeading = 0
        self.ent.desiredSpeed = 0
        self.keyboard = self.ent.engine.inputMgr.keyboard
        self.toggle = 0.15
	      
    def tick(self, dtime):
        self.keyboard.capture()
        selectedEnt = self.ent.engine.selectionMgr.selectedEnts[0]

        if self.toggle >= 0: 
            self.toggle -= dtime

            # Faster
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_UP):
            self.toggle = 0.15
            selectedEnt.desiredSpeed = utils.clamp(selectedEnt.desiredSpeed + selectedEnt.deltaSpeed, 0, selectedEnt.maxSpeed)

            # Slower
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_DOWN):
            self.toggle = 0.15
            selectedEnt.desiredSpeed = utils.clamp(selectedEnt.desiredSpeed - selectedEnt.deltaSpeed/5.5, 0, selectedEnt.maxSpeed)

            # turn left
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_LEFT):
            self.toggle = 0.15
            selectedEnt.desiredHeading += selectedEnt.deltaYaw
                #print "Control: ", str(selectedEnt), str(selectedEnt.desiredHeading)

            # turn right
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_RIGHT):
            self.toggle = 0.15
            selectedEnt.desiredHeading -= selectedEnt.deltaYaw
                #print "Control: ", str(selectedEnt), str(selectedEnt.desiredHeading)
            
       	selectedEnt.desiredHeading = utils.fixAngle(selectedEnt.desiredHeading)

class Control2(Aspect):
    def __init__(self, ent):
        Aspect.__init__(self, ent)

    def initialize(self):
        self.ent.desiredHeading = 0
        self.ent.desiredSpeed = 0
        self.keyboard = self.ent.engine.inputMgr.keyboard
        self.toggle = 0.15
        

    def tick(self, dtime):
        self.keyboard.capture()
        selectedEnt2 = self.ent.engine.selectionMgr.selectedEnts[1]

        if self.toggle >= 0: 
            self.toggle -= dtime

        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_W):
            self.toggle = 0.15
            selectedEnt2.desiredSpeed = utils.clamp(selectedEnt2.desiredSpeed + selectedEnt2.deltaSpeed, 0, selectedEnt2.maxSpeed)

            # Slower
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_S):
            self.toggle = 0.15
            selectedEnt2.desiredSpeed = utils.clamp(selectedEnt2.desiredSpeed - selectedEnt2.deltaSpeed/5.5, 0, selectedEnt2.maxSpeed)

            # turn left
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_A):
            self.toggle = 0.15
            selectedEnt2.desiredHeading += selectedEnt2.deltaYaw
                #print "Control: ", str(selectedEnt), str(selectedEnt.desiredHeading)

            # turn right
        if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_D):
            self.toggle = 0.15
            selectedEnt2.desiredHeading -= selectedEnt2.deltaYaw
                #print "Control: ", str(selectedEnt), str(selectedEnt.desiredHeading)
            
       	selectedEnt2.desiredHeading = utils.fixAngle(selectedEnt2.desiredHeading)


