#!/usr/bin/python

'''
Copyright (C) 2014 by Shahar Zeira (shahar.zeira@gmail.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from SysViewModel import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import math
import threading
import gobject
import time
import gc

gobject.threads_init()

gcIndex=0

CopyGuiDataCpu="CopyGuiDataCpu"
CopyGuiDataMemory="CopyGuiDataMemory"
ChangeGuiData="ChangeGuiData"

cpusDataArrayCopy=[]
memoryDataArrayCopy=[]

majorFormatter = FormatStrFormatter('%d')
minorLocatorY   = MultipleLocator(10)

detailsCpusLines = []
lock = threading.Lock()
xRange = range(LEN_Y_CHART)

class FuncThread(threading.Thread):
    def __init__(self, target):
        self._target = target
        threading.Thread.__init__(self)
    def run(self):
	self._target()

def setLine(place, name):
    ax = plt.subplot(place)
    ax.set_xlim((0, LEN_Y_CHART - 1))
    ax.set_ylim((0, 100))
    ax.set_xlabel(name)
    ax.set_xticks([])
    ax.yaxis.set_minor_locator(minorLocatorY)
    ax.yaxis.set_minor_formatter(majorFormatter)
    return ax

def changeGuiData(key):
    with lock:
	if key==CopyGuiDataCpu:
	    for i in rangeYChart:
		cpusDataArrayCopy[0][i]=cpuDataArray[i]
	    for i in rangeCpus:
		for j in rangeYChart:
		    cpusDataArrayCopy[1][i][j]=cpusDataArray[i][j]
	if key==CopyGuiDataMemory:
	    for i in rangeYChart:
		memoryDataArrayCopy[i]=memoryDataArray[i]
	if key==ChangeGuiData:
	    updateRecentMemoryDataArray()
	    updateRecentCpuDataArray()

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    for i in rangeCpus:
	detailsCpusLines[i].set_data([], [])
    return detailsCpusLinesTup

# animation function.  This is called sequentially
def animate(i):
    changeGuiData(CopyGuiDataCpu)
    line.set_data(xRange, cpusDataArrayCopy[0])

    for j in rangeCpus:
	detailsCpusLines[j].set_data(xRange, cpusDataArrayCopy[1][j])
    return detailsCpusLinesTup

# initialization function: plot the background of each frame
def initMemory():
    lineMemory.set_data([], [])
    return lineMemoryTup

# animation function.  This is called sequentially
def animateMemory(i):
    changeGuiData(CopyGuiDataMemory)
    lineMemory.set_data(xRange, memoryDataArrayCopy)
    return lineMemoryTup

wasThreaded=False
def updateLineDataGobject():
    global wasThreaded
    if not wasThreaded:
	t1 = FuncThread(updateLineDataThread)
	t1.daemon=True
	t1.start()
    time.sleep(myInterval/1000)
    return True

def updateLineDataThread():
    global wasThreaded
    global gcIndex
    wasThreaded=True
    while True:
	if gcIndex>60*1.7:
	    gcIndex=0
	    gc.collect()
	t1 = FuncThread(updateLastSysDictList)
	t1.daemon=True
	t1.start()

	updateLastSysDictMemory()
	updateLastSysDict()
	
	changeGuiData(ChangeGuiData)
	time.sleep(myInterval/1000/2)
	gcIndex+=1

initViewModel()
if len(cpusDataArrayCopy)==0:
    cpusDataArrayCopy.append(list(cpuDataArray))
    cpusDataArrayCopy.append([list(cpusDataArray[j]) for j in rangeCpus])

if len(memoryDataArrayCopy)==0:
    for i in rangeYChart:
	memoryDataArrayCopy.append(memoryDataArray[i])

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
fig.canvas.set_window_title('System Monitor') 

ax = setLine(211, "Cpu %")
line, = ax.plot([], [], lw=5)

for i in rangeCpus:
    ln, = ax.plot([], [], lw=1)
    detailsCpusLines.append(ln)
detailsCpusLines.append(line)
detailsCpusLinesTup=tuple(detailsCpusLines)

axMemory = setLine(212, "Memory % of total [" + str(lastSysDict[TOTAL_MEMORY]) + "]")
lineMemory, = axMemory.plot([], [], lw=5)
lineMemoryTup=tuple([lineMemory])

# call the animator.  blit=True means only re-draw the parts that have changed.
# Animate Memory usage
animMemory = animation.FuncAnimation(fig, animateMemory, init_func=initMemory,
                               frames=40, interval=myInterval, blit=True)

# Animate Cpu usage
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=40, interval=myInterval, blit=True)
gobject.idle_add(updateLineDataGobject)
plt.show()
