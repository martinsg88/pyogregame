# Render code for renderables
# vel is rate of change of pos
# Sushil Louis
from aspect import Aspect
from thickCircle import ThickCircle

class Renderable(Aspect):
    def __init__(self, ent):
        Aspect.__init__(self, ent)
        self.node = None

    def initialize(self):
        # make scenenode for entity
        print "Renderable: ", self.ent.uiname, self.ent.mesh
        e = self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + str(self.ent.eid), self.ent.mesh)

        self.node = self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + str(self.ent.eid) + '_node', self.ent.pos)
        self.node.attachObject(e)

        self.selectionCircle = ThickCircle(self.ent.uiname + str(self.ent.eid) +'.selectionCircle', self.ent.engine.gfxMgr.sceneManager, (1,0,0), self.node)
        self.selectionCircle.setup(radius = self.ent.length, thickness = 2 )

        self.selectionCircle2 = ThickCircle(self.ent.uiname + str(self.ent.eid) +'.selectionCircle2', self.ent.engine.gfxMgr.sceneManager, (0,0,1), self.node)
        self.selectionCircle2.setup(radius = self.ent.length, thickness = 2 )

    def tick(self, dtime):
        # copy entity information to sceneNode
        self.node.setPosition(self.ent.pos)
        self.node.resetOrientation()
        self.node.yaw(self.ent.heading)

        #---------------------------------------------
        # decorate ent for selection
        #---------------------------------------------
        if self.ent.uiname == 'mfboat':
            self.selectionCircle.show()
        else:
            self.selectionCircle.hide()
        #---------------------------------------------
        # other decorations
        #---------------------------------------------

