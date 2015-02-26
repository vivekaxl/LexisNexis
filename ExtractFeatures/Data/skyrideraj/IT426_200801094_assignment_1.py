
# IT426 Assignment 1
#
# A python program which demonstartes the animation of 6 pandas, 3 to move 
# in clockwise and 3 to move in anti-clockwise direction.
#
# 
#
# Written by Anirvan Mandal
# August 2011
# 
# Compile with python 2.6 
# Panda 3D game engine ver. 1.7.2 required
#

#Importing libraries

import direct.directbase.DirectStart
from direct.task import Task
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import math
from direct.actor import Actor
import random

# loading the environment

scene=loader.loadModel("models/environment")
scene.reparentTo(render)


scene.setScale(0.25,0.25,0.25)
scene.setPos(-8,0,45)
scene.setHpr(0,90,0)

# fixing the camera position

def FixPosTask(task):
  base.camera.setPos(0,-70,0)
  return Task.cont

taskMgr.add(FixPosTask, "FixPosTask")


# Clockwise Panda 1

pandaActor1= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor1.loop("walk")
pandaActor1.setScale(0.005,0.005,0.005)
pandaActor1.reparentTo(render)
pandaActor1.setHpr(90,90,90)

def SpinPanda1(task):
  angledegrees = ((task.time*20)+90)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor1.setPos(9*math.sin(angleradians),0,9*math.cos(angleradians))
  pandaActor1.setHpr(90,(angledegrees),-90)
  return Task.cont

taskMgr.add(SpinPanda1, "SpinPandaTask1")

#Clockwise Panda 2

pandaActor2= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor2.loop("walk")
pandaActor2.setScale(0.005,0.005,0.005)
pandaActor2.reparentTo(render)
pandaActor2.setHpr(90,90,90)

def SpinPanda2(task):
  angledegrees = ((task.time*20)+210)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor2.setPos(9*math.sin(angleradians),0,9*math.cos(angleradians))
  pandaActor2.setHpr(90,(angledegrees),-90)
  return Task.cont
taskMgr.add(SpinPanda2, "SpinPandaTask2")

# Clockwise Panda 3

pandaActor3= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor3.loop("walk")
pandaActor3.setScale(0.005,0.005,0.005)
pandaActor3.reparentTo(render)
pandaActor3.setHpr(90,90,90)

def SpinPanda3(task):
  angledegrees = ((task.time*20)+330)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor3.setPos(9*math.sin(angleradians),0,9*math.cos(angleradians))
  pandaActor3.setHpr(90,(angledegrees),-90)
  return Task.cont

taskMgr.add(SpinPanda3, "SpinPandaTask3")

# Anti-Clockwise Panda 1

pandaActor4= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor4.loop("walk")
pandaActor4.setScale(0.005,0.005,0.005)
pandaActor4.reparentTo(render)
pandaActor4.setHpr(90,90,90)

def SpinPanda4(task):
  angledegrees = ((task.time*20)+45)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor4.setPos(6*math.cos(angleradians),0,6*math.sin(angleradians))
  pandaActor4.setHpr(90,-(angledegrees+90),-90)
  return Task.cont

taskMgr.add(SpinPanda4, "SpinPandaTask4")

# Anti-Clockwise Panda 2

pandaActor5= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor5.loop("walk")
pandaActor5.setScale(0.005,0.005,0.005)
pandaActor5.reparentTo(render)
pandaActor5.setHpr(90,90,90)

def SpinPanda5(task):
  angledegrees = ((task.time*20)+165)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor5.setPos(6*math.cos(angleradians),0,6*math.sin(angleradians))
  pandaActor5.setHpr(90,-(angledegrees+90),-90)
  return Task.cont

taskMgr.add(SpinPanda5, "SpinPandaTask5")

# Anti-Clockwise Panda 3

pandaActor6= Actor.Actor("models/panda-model",{"walk":"models/panda-walk4"})
pandaActor6.loop("walk")
pandaActor6.setScale(0.005,0.005,0.005)
pandaActor6.reparentTo(render)
pandaActor6.setHpr(90,90,90)

def SpinPanda6(task):
  angledegrees = ((task.time*20)+285)
  angleradians = angledegrees * (math.pi / 180.0)
  pandaActor6.setPos(6*math.cos(angleradians),0,6*math.sin(angleradians))
  pandaActor6.setHpr(90,-(angledegrees+90),-90)
  return Task.cont

taskMgr.add(SpinPanda6, "SpinPandaTask6")


run()
