from __future__ import division 
import sys
sys.dont_write_bytecode = True

myoptions = {'MaxWalkSat':{'maxTries':'50','maxChanges':'2000','threshold':'0.001','probLocalSearch':'0.25'},'SA':{'kmax':'1000','emax':'0'},
'GA':{'crossOverRate':'0.6','mutationRate':'0.1','elitism':'50','generation':'20'},'DE':{'repeat':100,'np':1000,'f':0.75,'cf':0.3},
'PSO':{'N':30,'W':1,'phi1':1.3,'phi2':2.7,'repeat':1000,'threshold':'0.001'},
'Seive':{'tries':'20','repeat':'6','intermaxlimit':'35','extermaxlimit':'35','threshold':'15','initialpoints':'1000','lives':'4','subsample':'10'}
,'MOEAD':{'threshold':20},
'Seive3':{'intermaxlimit':'10','extermaxlimit':'10','threshold':'1','depth':'2'},
'Seive2_T1':{'intermaxlimit':'10','extermaxlimit':'10','threshold':'1','depth':'1'},
'Seive2_V50':{'initialpoints':'1000','intermaxlimit':'10','extermaxlimit':'10','threshold':'1','depth':'2'},
'Seive3_I1':{'initialpoints':'1000','intermaxlimit':'50','extermaxlimit':'50','threshold':'5','depth':'2','subsample':'200'},
'Seive2_V50_1':{'initialpoints':'1000','intermaxlimit':'10','extermaxlimit':'10','threshold':'1','depth':'6','tgen':'10'},
'Seive2_V50_2':{'initialpoints':'1000','intermaxlimit':'10','extermaxlimit':'10','threshold':'1','depth':'6','tgen':'1'},
'Seive2_V50_3':{'initialpoints':'1000','intermaxlimit':'20','extermaxlimit':'20','threshold':'1','depth':'20','tgen':'1'},
'Seive7_2':{'tgen':'1000'},
'Seive2_Initial':{'tgen':'500'},
'DE2':{'initial':500}}
myModeloptions = {'Lives': 4,'a12':0.56}
myModelobjf = {'Viennet':3,'Schaffer':2, 'Fonseca':2, 'Kursawe':2, 'ZDT1':2,'ZDT3':2,'DTLZ7':20,'Schwefel':1,'Osyczka':2,'DTLZ1':20,'DTLZ2':10,'DTLZ3':10,'DTLZ4':10,'DTLZ5':10,'DTLZ6':10,'POM3':3,'XOMO':4, 'RandomForest':1}
