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

from SysModel import *

LEN_Y_CHART = 81
rangeYChart=range(LEN_Y_CHART)
cpuDataArray = deque([0] * LEN_Y_CHART, maxlen=LEN_Y_CHART)
memoryDataArray = deque([0] * LEN_Y_CHART,maxlen=LEN_Y_CHART)
cpusDataArray = []

def initViewModel():
    updateLastSysDictList()
    while updateLastSysDict() == False:
	time.sleep(0.1)
    for i in rangeCpus:
	cpusDataArray.append(deque([0] * LEN_Y_CHART,maxlen=LEN_Y_CHART))

    updateRecentCpuDataArray()
    updateLastSysDictMemory()
    updateRecentMemoryDataArray()

def updateRecentCpuDataArray():
    updateCpuDataArray(lastSysDict)

def updateCpuDataArray(d):
    cpuDataArray.append(d[CPU])
    for i in rangeCpus:
	cpusDataArray[i].append(float(d[CPUS_DETAILS][i]))

def updateRecentMemoryDataArray():
    updateMemoryDataArray(lastSysDict)

def updateMemoryDataArray(d):
    memoryDataArray.append(d[USED_MEMORY] / d[TOTAL_MEMORY] * 100)
