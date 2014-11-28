# 381 main engine

class Engine(object):
    '''
    The root of the global manager tree
    '''
    def __init__(self):
        self.entMgr = None
        self.gfxMgr = None
        self.netMgr = None
        self.selectionMgr = None
        self.inputMgr = None
        self.widgetMgr = None

        self.gameMgr = None
        import time
        self.oldTime = time.time() # Use time.clock() for windows
        self.runTime = 0;
        self.keepRunning = True
        pass

    def initialize(self):
        import entMgr
        self.entMgr = entMgr.EntMgr(self)
        self.entMgr.initialize()

        import gfxMgr
        self.gfxMgr = gfxMgr.GfxMgr(self)
        self.gfxMgr.initialize()

        import netMgr
        self.netMgr = netMgr.NetMgr(self)
        self.netMgr.initialize()

        import inputMgr
        self.inputMgr = inputMgr.InputMgr(self)
        self.inputMgr.initialize()

        import selectionMgr
        self.selectionMgr = selectionMgr.SelectionMgr(self)
        self.selectionMgr.initialize()

        import widgetMgr
        self.widgetMgr = widgetMgr.WidgetMgr(self)
        self.widgetMgr.initialize()

        import gameMgr
        self.gameMgr = gameMgr.GameMgr(self)
        self.gameMgr.initialize()


    def crosslink(self):
        self.entMgr.crosslink()
        self.gfxMgr.crosslink()
        self.netMgr.crosslink()
        self.inputMgr.crosslink()
        self.selectionMgr.crosslink()
        self.widgetMgr.crosslink()

        self.gameMgr.crosslink()


    def loadLevel(self):
        self.entMgr.loadLevel()
        self.gfxMgr.loadLevel()
        self.netMgr.loadLevel()
        self.inputMgr.loadLevel()
        self.selectionMgr.loadLevel()
        self.widgetMgr.loadLevel()
        self.gameMgr.loadLevel()

    def releaseLevel(self):
        self.entMgr.releaseLevel()
	print "test1"
        self.gfxMgr.releaseLevel()
	print "tes6"
        self.netMgr.releaseLevel()
	print "tes5"
        self.inputMgr.releaseLevel()
	print "tes4"
        self.selectionMgr.releaseLevel()
	print "tes3"
        self.widgetMgr.releaseLevel()
	print "tes2"
        self.gameMgr.releaseLevel()

    def stop(self):
        self.keepRunning = False

    def run(self):
        import time
        import ogre.renderer.OGRE as ogre
        weu = ogre.WindowEventUtilities() # Needed for linux/mac
        weu.messagePump()                 # Needed for linux/mac

        
        while (self.keepRunning):
            now = time.time() # Change to time.clock() for windows
            dtime = now - self.oldTime
            self.oldTime = now

            self.entMgr.tick(dtime)
            self.gfxMgr.tick(dtime)
            self.netMgr.tick(dtime)
            self.inputMgr.tick(dtime)
            self.selectionMgr.tick(dtime)
            self.widgetMgr.tick(dtime)
            self.gameMgr.tick(dtime)
            

            self.runTime += dtime
        
            weu.messagePump()             # Needed for linux/mac
            time.sleep(0.001)

        self.releaseLevel()
