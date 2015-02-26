
# IT426 Assignment 2
#
# A python program which demonstartes the animation of 3 dinosaurs in an environment. 
# T-rex is running around a rock
# A baby dinosaur is jumping around
# another big dinosaur is roaring
#
# Written by Anirvan Mandal
# August 2011
# 
# Compile with python 2.6 
# Panda 3D game engine ver. 1.7.2 required
#

from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from direct.task import Task
from panda3d.core import Point3
from direct.interval.IntervalGlobal import Sequence

class Application(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.disableMouse()#mouse disabled
        #rocky terrain load
        self.environ=loader.loadModel("models/environment")
        self.environ.reparentTo(render)
        self.environ.setScale(0.15,0.15,0.15)
        self.environ.setPos(0,-10,0)
        #loading the sky background
        self.sky=loader.loadModel("models/farmsky")
        self.sky.reparentTo(render)
        self.sky.setScale(0.3,0.3,0.3)
        self.sky.setPos(0,350,0)
        #baby dinosaur model
        self.babyd = Actor("babyd", {"sit": "babydani"})
        self.babyd.reparentTo(render)
        self.babyd.setPos(Vec3(25,-150, 3))
        self.babyd.loop("sit")
        #big dinosaur model
        self.bigd = Actor("bigd", {"roar": "bigdani"})
        self.bigd.reparentTo(render)
        self.bigd.setPos(Vec3(30, -110, 0))
        self.bigd.loop("roar")
        #trex model
        self.trex = Actor("trex", {"run": "trex-eat"})
        self.trex.reparentTo(render)
        self.trex.loop("run")
        self.trex.setHpr(270,0,0)
        self.cam.setPos(-20, -200, 22)
         #trex animation
        trexPosInterval1 = self.trex.posInterval(3,
                                                        Point3(-60,-120, 0),
                                                        startPos = Point3( -10,-120, 0))
        trexPosInterval2 = self.trex.posInterval(3,
                                                        Point3(-60,0, 0),
                                                        startPos = Point3( -60,-120, 0))
        trexPosInterval3 = self.trex.posInterval(3,
                                                        Point3(-10,0, 0),
                                                        startPos = Point3( -60,0, 0))
        trexPosInterval4 = self.trex.posInterval(3,
                                                        Point3(-10,-120, 0),
                                                        startPos = Point3( -10,0, 0))
        trexHprInterval1 = self.trex.hprInterval(0.5,
                                                        Point3(180, 0, 0),
                                                        startHpr = Point3(270, 0, 0))
        trexHprInterval2 = self.trex.hprInterval(0.5,
                                                        Point3(90, 0, 0),
                                                        startHpr = Point3(180, 0, 0))
        trexHprInterval3 = self.trex.hprInterval(0.5,
                                                        Point3(0, 0, 0),
                                                        startHpr = Point3(90, 0, 0))
        trexHprInterval4 = self.trex.hprInterval(0.5,
                                                        Point3(-90, 0, 0),
                                                        startHpr = Point3(0, 0, 0))
        
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(trexPosInterval1, trexHprInterval1,
                                  trexPosInterval2, trexHprInterval2,trexPosInterval3,trexHprInterval3,trexPosInterval4,trexHprInterval4,
                                  name="pandaPace")
        self.pandaPace.loop()
        


if __name__ == "__main__":
    gameApp = Application()
    gameApp.run()
    
