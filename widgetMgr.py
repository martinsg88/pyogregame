
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

from mgr import Mgr

from vector import Vector3, point2

class UIDefaults:
    POS = (0, 0)
    WIDTH = 200
    HEIGHT = 100

    PANEL_SIZE = (50, 10)
    PANEL_MATERIAL = "ECSLENT/navy/material/shipInfo/overlay"
    LINE_SEP_MATERIAL  = "ECSLENT/line"

    LABEL_SIZE = (50, 10)
    LABEL_X_OFFSET = 5
    LABEL_Y_OFFSET = 5
    LABEL_TEXT_COLOR = (1.0, 1.0, 0.7)

    BUTTON_SIZE = (50, 20)
    BUTTON_OFF_TEXT_COLOR = (1.0, 1.0, 0.0)
    BUTTON_ON_TEXT_COLOR  = (0.0, 0.0, 0.5)

    MENU_ITEM_SIZE = (20, 10)
    MENU_DEFAULT_TEXT_COLOR = (1.0, 1.0, 0.0)
    MENU_SELECTED_TEXT_COLOR = (1.0, 1.0, 6.5)
    MENU_MATERIAL = "ECSLENT/navy/material/rmenu"


class Widget (object):
    """Top level UI object. Needs engine passed in
    """
    def __init__(self, engine, parent = None, pos=None, size=None):
        if pos is None: #if we default parameter these all objects will share a common instantiation which WILL cause nightmares
            pos = point2(0,0)
        if size is None: #if we default parameter these all objects will share a common instantiation which WILL cause nightmares
            #size = point2(100,13)
            size = point2(100,20)

        #EngineObject.__init__(self, engine)
        assert engine is not None
        if type(pos) is tuple:
            pos = point2(*pos)
        if type(size) is tuple:
            size = point2(*size)

        self._pos = pos
        self._size = size
        self.engine = engine
        self.parent = parent

    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.posChanged()
    def posChanged(self):
        pass

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
        self.sizeChanged()
    def sizeChanged(self):
        pass

    @property
    def width(self):
        return self._size.x
    @width.setter
    def width(self, val):
        self.size = point2(val, self.size.y)

    @property
    def height(self):
        return self._size.y
    @height.setter
    def height(self, val):
        self.size = point2(self.size.x, val)
           

    @property
    def screenPos(self):
        if self.parent:
            return self.parent.screenPos + self.pos
        else:
            return self.pos

    def cursorInMe(self, mx, my):
        ax, ay = (self.screenPos.x, self.screenPos.y)
        return ((mx >= ax) and (mx <= ax + self.width) and (my >= ay) and (my <= ay + self.height))




class Panel(Widget):
    """
    """
    class Placement:
        Below = 0
        Right = 1

    def __init__(self, engine, parent = None, name = "ex.Panel", pos = (0.0, 0.0), size = UIDefaults.PANEL_SIZE, material = None):
        Widget.__init__(self, engine, parent = parent, pos = pos, size = size)
        self.overlayManager = ogre.OverlayManager.getSingleton()

        self.pid         = name + str(engine.widgetMgr.getNextId())
        self.panel       = self.overlayManager.createOverlayElement("Panel", self.pid)
        self.panel.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        self.panel.setPosition(self.pos.x, self.pos.y)
        #self.panel.setDimensions(self.width, self.height)
        self.height = 50 # otherwise, the panel has extra height when using as a parent for labels and other widgets.
        self.panel.setDimensions(self.width, self.height)
        if material:
            self.panel.setMaterialName(material)

        self.panel.show()        

        if not self.parent:
            self.id = name
            self.overlayName = name + str(engine.widgetMgr.getNextId())
            self.overlay     = self.overlayManager.create(self.overlayName)
            self.overlay.add2D(self.panel)
            self.overlay.show()
            #print "---------> Created overlay and added panel to overlay: ",  self.overlayName

        self.panel.show()

        self.belowPos = point2(0,0)
        self.rightPos = point2(0,0)
        self.xgap = 0
        self.ygap = 0
        self._items = []

        self.lheight = 1
        self._linePanels = [] # used by menu items
        self.addSep(0)
        pass

    def linePanel(self):
        lid = self.pid + "line/" + str(self.engine.widgetMgr.getNextId())
        lp = self.overlayManager.createOverlayElement("Panel", lid)
        lp.setMetricsMode(ogre.GMM_PIXELS)#RELATIVE_ASPECT_ADJUSTED)
        lp.setPosition(0, 0)
        lp.setDimensions(self.width, self.lheight)
        #lp.setMaterialName("ECSLENT/line")
        lp.show()
        return lp
 
    def addSep(self, y):
        lp = self.linePanel()
        self._linePanels.append(lp)
        lp.setPosition(0, y) # lineSep, 0, 0
        self.panel.addChild(lp)

    def adjustSeps(self):
        '''
        QUEST: What is this? - cmiles
        '''
        for lp in self._linePanels:
            lp.setDimensions(self.width, self.lheight)

    def render(self):
        for item in self._items:
            item.render()

    def show(self):
        if not self.parent:
            self.overlay.show()
        self.panel.show()
        for item in self._items:
            item.show()

    def hide(self):
        for item in self._items:
            item.hide()
        self.panel.hide()
        if not self.parent:
            self.overlay.hide()

    def posChanged(self):
        self.panel.setPosition(self.pos.x, self.pos.y)
        for item in self._items:
            item.posChanged()

    def addItem(self, item, func = None, placement = Placement.Below):
        self._items.append(item)
        if(self.width < item.width):
            self.width = item.width
            self.adjustSeps()

        #pdb.set_trace()
        if placement == Panel.Placement.Below:
            item.pos = self.belowPos
            self.rightPos = self.belowPos + point2(item.width + self.xgap, 0)
            self.belowPos = point2(0, self.belowPos.y + item.height + self.ygap)

        elif placement == Panel.Placement.Right:
            item.pos = self.rightPos
            self.rightPos = self.rightPos + point2(item.width + self.xgap, 0)

        if self.rightPos.x > self.width:
            self.width = self.rightPos.x

        if self.belowPos.y > self.height:
            self.height = self.belowPos.y
        #self.height += item.height

        #print 'Panel.addItem', self, item, placement, item.pos, self.belowPos, self.rightPos

        self.panel.addChild(item.getOverlayElementToAdd())

        self.panel.setDimensions(self.width, self.height)
        self.addSep(self.height)

    def deleteItem(self, item):
        item.hide()
        self._item.remove(element)

    def getItems(self):
        return self._items

    def getOverlayElementToAdd(self):
        return self.panel


class Label(Widget):
    '''
    '''
    def __init__(self, engine, parent = None, caption = "Ex.Label", color = (5.0, 5.0, 5.0), size = UIDefaults.LABEL_SIZE, pos = (0, 0)):
        '''
        '''
        Widget.__init__(self, engine, parent = parent, pos = pos, size = size)
        self.overlayManager =  ogre.OverlayManager.getSingleton()
        self.caption = caption
        self.color   = color

        self.xOffset = 5
        self.yOffset = 2

        self.id = "ECSLENT/Label/" + str(self) + "/" + caption  + "/" + str(engine.widgetMgr.getNextId())
        self.textArea = self.overlayManager.createOverlayElement("TextArea", self.id)
        self.textArea.setMetricsMode(ogre.GMM_PIXELS)
        self.textArea.setCaption(caption)
        self.textArea.setPosition(self.pos.x  + self.xOffset, self.pos.y + self.yOffset)
        self.textArea.setDimensions(self.width, self.height)
        self.textArea.setFontName("BlueHighway")
        self.textArea.setCharHeight(50)
        self.textArea.setColour(self.color)
        self.textArea.show()

        #textArea.setColourTop((1.0, 1.0, 0.7))
        #textArea.setColourBottom((1.0, 1.0, 0.7))

    def render(self):
        pass

    def tick(self, dtime):
        pass
#-------------------------------------------------------------------
    def getTextArea(self):
        return self.textArea
#-------------------------------------------------------------------
    def getOverlayElementToAdd(self):
        return self.textArea
#-------------------------------------------------------------------
    def show(self):
        self.textArea.show()
#-------------------------------------------------------------------
    def hide(self):
        self.textArea.hide()
#-------------------------------------------------------------------
    def setCaption(self, caption):
        self.caption = caption
        self.textArea.setCaption(self.caption)
#-------------------------------------------------------------------
    def getCaption(self):
        return self.caption

    def posChanged(self):
        #print 'Label.posChanged', self.pos, self.screenPos
        self.textArea.setPosition(self.pos.x + self.xOffset, self.pos.y + self.yOffset)

    def sizeChanged(self):
        #print 'Label.sizeChanged', self.size
        self.textArea.setDimensions(self.width, self.height)

    def setCharHeight(self, height):
        self.height = height
        self.setCharHeight(height)

class LabelPair(Panel):
    """
    About 90% of the time we use labels in pairs
    the first is a fixed piece of text describing what the second is
    the second being the actual data we are representing - which varies over time
    """
    def __init__(self, engine, parent, label1Text, label2Text='', columnWidths=(100,200), columnHeightPixels = UIDefaults.PANEL_SIZE[1]):
        Panel.__init__(self, engine, parent=parent, pos=(0,0), size=(columnWidths[0] + columnWidths[1], columnHeightPixels))
        self.label1 = Label(engine, parent=self, caption=label1Text, pos=(0,0), size=(columnWidths[0], columnHeightPixels))
        self.addItem(self.label1, placement=Panel.Placement.Below)
        self.label2 = Label(engine, parent=self, caption=label2Text, pos=(columnWidths[0],0), size=(columnWidths[1], columnHeightPixels))
        self.addItem(self.label2, placement=Panel.Placement.Right)

    @property
    def leftCaption(self):
        self.label1.caption
    @leftCaption.setter
    def leftCaption(self, caption):
        self.label1.setCaption(caption)

    @property
    def rightCaption(self):
        self.label2.caption
    @leftCaption.setter
    def rightCaption(self, caption):
        self.label2.setCaption(caption)


    @property
    def caption(self):
        return self.caption
    @caption.setter
    def caption(self, caption):
        self.label2.setCaption(caption)


class FramerateWidget(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Framerate: ", pos = (350, 1), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("Welcome to Monster Boat!")

    def render(self):
        pass

class Player1(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Player 2 (white) : ", pos = (800, 800), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
	pass

    def render(self):
        pass

class Player1Score(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Score: ", pos = (800, 860), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("Score: %5i" % self.engine.gameMgr.ent1.score)
	pass

    def render(self):
        pass

class Player2(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Player 1 (red) : ", pos = (1, 800), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
	pass

    def render(self):
        pass

class Player2Score(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "Player 2: ", pos = (1, 860), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("Score: %5i" % self.engine.gameMgr.ent2.score)
	pass

    def render(self):
        pass

class Player2HP(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "HP: ", pos = (1, 920), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("HP: %8i" % self.engine.gameMgr.ent2.health)
	pass

    def render(self):
        pass

class Player1HP(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "HP: ", pos = (800, 920), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("HP: %8i" % self.engine.gameMgr.ent1.health)
	pass

    def render(self):
        pass



class PopUp1(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "", pos = (500, 500), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("Player 2 Wins!")
	pass

    def render(self):
        pass


class PopUp2(Panel):
    '''Displays and updates framerate
    '''
    def __init__(self, engine, name = "", pos = (500, 500), size = (100, 13)):
        Panel.__init__(self, engine, name = name, pos = pos, size = size)
        self.label = Label(engine, caption = name, pos = (0,0), size = size)
        self.addItem(self.label)
        self.show()
        self.label.show()
        
    def tick(self, dtime):
        stats = self.engine.gfxMgr.renderWindow.getStatistics()
        self.label.setCaption("Player1 Wins!")
	pass

    def render(self):
        pass


class WidgetMgr(Mgr):
    widgets = []
    idCounter = 0

    def __init__(self, engine):
        Mgr.__init__(self, engine)
        self.x = 0


    def crosslink(self):
        pass

    def initialize(self):
        self.framerateWidget = FramerateWidget(self.engine)
        self.widgets.append(self.framerateWidget)

        self.Player1= Player1(self.engine)
        self.widgets.append(self.Player1)

        self.Player2= Player2(self.engine)
        self.widgets.append(self.Player2)

        self.Player1Score= Player1Score(self.engine)
        self.widgets.append(self.Player1Score)

        self.Player2Score= Player2Score(self.engine)
        self.widgets.append(self.Player2Score)

	self.Player1HP = Player1HP(self.engine)
	self.widgets.append(self.Player1HP)

	self.Player2HP = Player2HP(self.engine)
	self.widgets.append(self.Player2HP)


    def tick(self, dtime):
        for widget in self.widgets:
            widget.tick(dtime)
	    if (self.engine.gameMgr.ent1.score >= 1500 or (self.engine.gameMgr.ent1.health == 0)):
	        PopUp1(self.engine).tick(dtime)
		self.engine.gameMgr.ent1.desiredSpeed *= 0
		self.engine.gameMgr.ent2.desiredSpeed *= 0
	    elif (self.engine.gameMgr.ent2.score >= 1500 or (self.engine.gameMgr.ent2.health == 0)):
	        PopUp2(self.engine).tick(dtime)
		self.engine.gameMgr.ent1.desiredSpeed *= 0
		self.engine.gameMgr.ent2.desiredSpeed *= 0

    def render(self):
        for widget in self.widgets:
            widget.render()


    xzPlane = ogre.Plane((0, 1, 0), 0)
    def findWorldCoords(self, ms):
        ''' Map to x,z plane from viewport
        '''
        ms.width = self.engine.gfxSystem.viewport.actualWidth 
        ms.height = self.engine.gfxSystem.viewport.actualHeight
        mouseRay = self.engine.cameraSystem.camera.getCameraToViewportRay(ms.X.abs/float(ms.width), ms.Y.abs/float(ms.height))
        result  =  mouseRay.intersects(self.xzPlane)
        pos = None
        if result.first:
            pos =  mouseRay.getPoint(result.second)
            #self.mousePosWorld = pos
        return pos


    
    def getNextId(self):
        self.idCounter += 1
        return self.idCounter
