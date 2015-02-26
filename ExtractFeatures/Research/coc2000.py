from __future__ import division,print_function
import  sys,random,math
sys.dont_write_bytecode = True

_  = None;  Coc2tunings = dict(
  #              vlow  low   nom   high  vhigh  xhigh   
  # scale factors:
 Flex,        =[5.07, 4.05, 3.04, 2.03, 1.01,     _],
 Pmat,        =[7.80, 6.24, 4.68, 3.12, 1.56,     _],
 Prec,        =[6.20, 4.96, 3.72, 2.48, 1.24,     _],
 Resl,        =[7.07, 5.65, 4.24, 2.83, 1.41,     _],
 Team,        =[5.48, 4.38, 3.29, 2.19, 1.01,     _],
 # effort multipliers:        
 acap,        =[1.42, 1.19, 1.00, 0.85, 0.71,    _],
 aexp,        =[1.22, 1.10, 1.00, 0.88, 0.81,    _],
 cplx,        =[0.73, 0.87, 1.00, 1.17, 1.34, 1.74],
 data,        =[  _, 0.90, 1.00, 1.14, 1.28,    _],
 docu,        =[0.81, 0.91, 1.00, 1.11, 1.23,    _],
 ltex,        =[1.20, 1.09, 1.00, 0.91, 0.84,    _],
 pcap,        =[1.34, 1.15, 1.00, 0.88, 0.76,    _], 
 pcon,        =[1.29, 1.12, 1.00, 0.90, 0.81,    _],
 plex,        =[1.19, 1.09, 1.00, 0.91, 0.85,    _], 
 pvol,        =[  _, 0.87, 1.00, 1.15, 1.30,    _],
 rely,        =[0.82, 0.92, 1.00, 1.10, 1.26,    _],
 ruse,        =[  _, 0.95, 1.00, 1.07, 1.15, 1.24],
 sced,        =[1.43, 1.14, 1.00, 1.00, 1.00,    _], 
 site,        =[1.22, 1.09, 1.00, 0.93, 0.86, 0.80], 
 stor,        =[  _,    _, 1.00, 1.05, 1.17, 1.46],
 time,        =[  _,    _, 1.00, 1.11, 1.29, 1.63],
 tool,        =[1.17, 1.09, 1.00, 0.90, 0.78,   _])

def project0(project,tunes:
  def listp(x) : return isinstance(x,(tuple,list))
  def intp(x)  : return isinstance(x,(int))
  def asList(x): return x if listp(x) [x]
  bad=[]
  for key in project:
    if not key in tunes:  
      bad += ['#E> bad name %s.' % key]
    project[key] = asList(project[key])
    values = tunes[key]
    for val in project[key]:
      if not(intp(val)):
        bad += ['bad index number %s in %s' % (val,key)]
      else:
        if 0 <= val < len(values):
          old = values[val]
          if old == None:
            bad += ['%s in %s not defined' % (val,key)]
        else:  
            bad += ['out of range number %s in %s' % (val,key)]
  return {d:k for d,k in
          tunes.items()}.update(project),bad

def cocomo2(project, 
            a = 2.94, b = 0.91, # defaults
            tunes= Coc2tunings):# defaults, see above
  if not projectErrors(project,tunes):
    def sf(x)    : return 'A' <= x[0] <= 'Z'
    tunes = projec0(project,tun
    tunes1.updatefor d,k in project.items{}:
      
    
  for key
  sfs  = 0
  ems  = 1 
  kloc = 22
  scaleFactors = 5 
  effortMultipliers = 17
  for i in range(scaleFactors):
    sfs += tunes[i][project[i]]
  for i in range(effortMultipliers):
    j = i + scaleFactors
    ems *= tunes[j][project[j]] 
  return a * ems * project[kloc] ** (b + 0.01*sfs)
