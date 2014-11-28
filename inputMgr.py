# Input manager. Initialize and manage keyboard and mouse. Buffered and unbuffered input
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS


from mgr import Mgr
from vector import Vector3

from unitAI import UnitAI
from command import Target, Move, Ram

class InputMgr(Mgr, OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        Mgr.__init__(self, engine)
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)
        self.move = 250
        self.rotate = 0.01
        self.yawRot = 0.0
        self.pitchRot = 0.0
        self.transVector = ogre.Vector3(0, 0, 0)
        self.toggle = 0.1
        self.distanceSquaredThreshold = 10000
        self.leftShiftDown = False;
        pass

    def initialize(self):
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeInt("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]
        paramList.append(("x11_mouse_grab", "false"))
        paramList.append(("x11_mouse_hide", "false"))
        paramList.append(("x11_keyboard_grab", "false"))
        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        self.keyboard = None
        self.mouse    = None
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
        except Exception, e:
            print "No Keyboard or mouse!!!!"
            raise e
        if self.keyboard:
            self.keyboard.setEventCallback(self)
        if self.mouse:
            self.mouse.setEventCallback(self)
 
        self.transVector = ogre.Vector3(0, 0, 0)

        import random
        self.randomizer = random
        self.randomizer.seed(None)

        self.mouse.capture();
        ms = self.mouse.getMouseState()
        ms.width = self.engine.gfxMgr.viewPort.actualWidth
        ms.height = self.engine.gfxMgr.viewPort.actualHeight

        print "Initialized Input Manager"
        

    def crosslink(self):
        self.camera = self.engine.gfxMgr.camera
        self.camYawNode = self.engine.gfxMgr.camYawNode
        self.camPitchNode = self.engine.gfxMgr.camPitchNode


    def releaseLevel(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        
    def tick(self, dtime):
        self.keyboard.capture()
        self.mouse.capture()

        self.keyPressed(dtime)
        
        #self.camNode.yaw(ogre.Degree(-self.yawRot)
        self.camYawNode.yaw(ogre.Radian(self.yawRot))
        self.camPitchNode.pitch(ogre.Radian(self.pitchRot))

        # Translate the camera based on time.
        self.camYawNode.translate(self.camYawNode.orientation
                               * self.transVector
                               * dtime)

        self.handleCreateEnt(dtime)
        pass

    def handleCreateEnt(self, dt):
        self.toggle = self.toggle - dt
        if self.keyboard.isKeyDown(OIS.KC_EQUALS) and self.toggle < 0.0:
            ent = self.engine.entMgr.createEnt(self.randomizer.choice(self.engine.entMgr.entTypes), pos = Vector3(0,0,0))
            self.toggle = 0.1

    def keyPressed(self, evt):
        # Move the camera using keyboard input.
        self.transVector = ogre.Vector3(0, 0, 0)
        self.yawRot = 0.0
        self.pitchRot = 0.0
	if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.stop()

	if self.keyboard.isKeyDown(OIS.KC_R):
            self.engine.releaseLevel()
	    self.engine.initialize()
	    self.engine.crosslink()
	    self.engine.loadLevel()
	    self.engine.run()

        return True

    def keyReleased(self, evt):
        return True
    
       # MouseListener
    def mouseMoved(self, evt):
        #self.entUnderMouse = None
        return True

    def mousePressed(self, evt, id):
        if id == OIS.MB_Left:
            self.doSelection()
        elif id == OIS.MB_Right:
            self.doAction()

        return True

    def posUnderMouse(self):
        self.mouse.capture()
        ms = self.mouse.getMouseState()
        mousePos = (ms.X.abs/float(ms.width), ms.Y.abs/float(ms.height))
        mouseRay = self.camera.getCameraToViewportRay(*mousePos)
        result = mouseRay.intersects(self.engine.gfxMgr.groundPlane)
        if result.first:
            pos = mouseRay.getPoint(result.second)
            return pos
        else:
            return None

    def doSelection(self):
        pos = self.posUnderMouse()

        if pos:
            print "World Pos: ", pos.x, pos.y, pos.z
            ent = self.findClosestEntWithinThresholdDistanceSquared(pos)
            '''if ent:
                if self.leftShiftDown:
                    self.engine.selectionMgr.addSelection(ent)
                else:
                    self.engine.selectionMgr.setSelection(ent)
'''
    def findClosestEntWithinThresholdDistanceSquared(self, pos):
        if not self.engine.entMgr.ents:
            return None

       # print "Finding closest ents to", str(pos)
        minEnt = self.engine.entMgr.ents[0]
        minDist = minEnt.pos.squaredDistance(pos)
        for id, ent in self.engine.entMgr.ents.iteritems():
            sqdist = ent.pos.squaredDistance(pos)
            if sqdist < minDist:
                minDist = sqdist
                minEnt  = ent

        if minDist <= self.distanceSquaredThreshold:
            return minEnt
        else:
            return None
                
            
    def doAction(self):
        print "Doing action"
        self.entUnderMouse = None
        posUnderMouse = self.posUnderMouse()
        if posUnderMouse:
            self.entUnderMouse = self.findClosestEntWithinThresholdDistanceSquared(posUnderMouse)

            if self.entUnderMouse:
                self.doRam(self.entUnderMouse)
            else:
                self.doMove(posUnderMouse)
        pass

    def doRam(self, targetEnt):

        for ent in self.engine.selectionMgr.selectedEnts:
            asp = ent.findAspect(UnitAI)
            if self.leftShiftDown:
                asp.addCommand(Ram(ent, Target(targetEnt, None)))
            else:
                asp.setCommand(Ram(ent, Target(targetEnt, None)))

        pass
    

    def doMove(self, pos):
        for ent in self.engine.selectionMgr.selectedEnts:
            asp = ent.findAspect(UnitAI)
            if self.leftShiftDown:
                asp.addCommand(Move(ent, Target(None, pos)))
            else:
                asp.setCommand(Move(ent, Target(None, pos)))                

    def mouseReleased(self, evt, id):
        return True
    
       # JoystickListener
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True

#---------------------------------------------------------------------------------------------------
