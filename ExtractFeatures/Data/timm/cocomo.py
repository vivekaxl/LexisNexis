"""
This file was documented using references from the handout COCOMO II.
Model Definition and http://sunset.usc.edu/research/COCOMOII/expert_cocomo.
"""
from __future__ import division
import sys,random
sys.dont_write_bytecode=True
rand=random.random
seed=random.seed
any  = random.choice

class Value:
  def __init__(i,f): 
    i._x, i.f = None, f
  def tell(i,value=None): 
    i._x = value
  def ask(i): 
    if i._x == None: 
      i._x = i.f()
    return i._x

def biased(a,b,bias=2):
  return Value(lambda: a + (b-a)*(rand()**bias))
def has(a,b) : 
  return Value(lambda: a + (b-a)*rand())
def of(a,b): 
  return Value(lambda: a + any(range(0,b-a+1)))
def val(a):
  return Value(lambda : a)

def gets(it,lst):
  t   = tunings()
  out = [get(it,this,t) for this in lst]
  return out[0] if len(out)==1 else out

def get(it,this,t=None):
  t = t or tunings() 
  y = it[this].ask()
  return t[this][y-1] if this in t else y
  
def prod(lst):
  if not lst: return 0
  out = lst[0]
  for x in lst[1:]: out *= x
  return out
   
class Candidate:
  def __init__(i,obj={},dec={}):
    i.objs,i.decs=d1,d2
    i.obj=[None]*len(d1.keys())
    i.dec=[None]*len(d2.keys())

def cocomos(**updates):
  return constrain(updates, dict(
    # calibration parameters
    a=has(2.25,3.25), # tuning for linear effects
    b=has(0.9, 1.1),  # tuning for exponential effects   
    c=has(3.0, 3.67),
    d=has(0.28, 0.33),
    newKsloc=has(2, 10000),# thousands of lines of codes
    adaptedKsloc=biased(2,10000,bias=3),
    revl    = biased(0,100,bias=3),
    aa      = biased(0,100,bias=3), # LOOK UP
    su      = biased(0,100,bias=0.3),  # LOOK UP
    unfm    = biased(0,100,bias=3),  # LOOK UP
    dm      = biased(0,100,bias=3),
    cm      = biased(0,100,bias=3),
    at      = biased(0,100,bias=3),
    im      = biased(0,100,bias=3),
    atKProd = biased(0,100,bias=0.3),
    #--- scale factors: exponential effect on effort ----
    prec    = of(1, 5), # Precedentedness
    flex    = of(1, 5), # Development Flexibility
    resl    = of(1, 5), # Architecture/Risk Resolution
    team    = of(1, 5), # Team Cohesion
    pmat    = of(1, 5), # Process Maturity
    #--- effort multipliers: linear effect on effort ----
    # Product Factors:
    rely=of(1, 5), # Required Software Reliability 
    data=of(2, 5), # Data Base Size
    cplx=of(1, 6), # Product Complexity
    ruse=of(2, 6), # Required Reusability
    docu=of(1, 5), # Documentation Match to Life-Cycle Needs
    # Platform Factors:
    time=of(3, 6), # Execution Time Constraint
    stor=of(3, 6), # Main Storage Constraint
    pvol=of(2, 5), # Platform Volatility
    # Personnel Factors:
    acap=of(1, 5), # Analyst Capability
    pcap=of(1, 5), # Programmer Capability
    pcon=of(1, 5), # Personnel Continuity
    aexp=of(1, 5), # Applications Experience
    plex=of(1, 5), # Platform Experience
    ltex=of(1, 5), # Language and Tool Experience
    # Project Factors:
    tool=of(1, 5), # Use of Software Tools
    site=of(1, 6), # Multi-site Development
    sced=of(1, 5), # Schedule pressure
    # defect removal methods
    automated_analysis = of(1, 6),
    peer_reviews = of(1, 6),
    execution_testing_and_tools = of(1, 6)
    ))
 
def cocomo2000(it=cocomos()):
  """Estimate calculates the quotient result from 
  dividing the person-month calculation, pm(), 
  by the amount of calendar time necessary to 
  develop the product, tdev()."""
  def x(*y):
    "Hook into data lookup"
    return gets(it,y)

  def size():
    """Size displays the overall size of the product.
    It is calculated from  the percentage of code 
    discarded, revl(), the new source lines of code,
    newsKsloc(), and the calculation of code reuse, 
    equivalentKsloc().
    """
    return (1+( x('revl') /100)) \
        * (x('newKsloc')+equivalentKsloc())
  def equivalentKsloc():
    """EquivalenKsloc is the calculation of code reuse.  It is derived from the
    size of the adapted component in thousands of adapted source lines of code,
    adaptedKsloc(), the adaptation adjustment modifier, aam(), and the
    percentage of code that is reengineered by automatic translation, at()."""
    return x('adaptedKsloc')*aam()*(1-(x('at')/100))
  def aam():
    """#aam is the adaptation adjustment modifier that returns the result of one
    of two calculations based on the value of the adaptation adjustment factor,
    aaf().  aam is calculated from the degree of assessment and assimilation,
    aa(), the adaptation adjustment factor, aaf(), the software understanding,
    su(), and the programmer's unfamiliarity with the software, unfm(). 
    This function was changed from the original version that contained errors.
    """
    f = aaf()
    if f <= 50 :
      return (x('aa')+f*(1+(0.02*x('su')*x('unfm'))))/100
    else :      
      return (x('aa')+f*(x('su')*x('unfm')))/100
  def aaf():
    """aaf is the adaptation adjustment factor and is calculated using the percentage
    of the adapted software's design that is modified, dm(), the percentage of
    code modified, cm(), and the percentage of effort necessary to integrate
    the reused software, im(). """
    return 0.4*x('dm')+0.3*x('cm')+0.3*x('im')
  def  scedPercent():
    """scedPercent is the compression/expansion percentage in the sced effort
    multiplier rating scale. These values reflect the rating scale from
    Table 2.34, page 51 of the handout.  This function was added to the original 
    version. """ 
    y=x("sced")
    return [75,85,100,130,160][int(round(y))]
  def tdev():
    """tdev is the amount of calendar time necessary to develop the product. It
    is calculated using the constant c(), the amount of effort in person-months, 
    pmNs(), the exponent used in the tdev function, f(), and the compression/
    expansion percentage in the sced effort multiplier rating scale,  
    scedPercent(). """
    return (x('c')*(pmNs()**f()))*scedPercent()/100
  def f():
    """f is the exponent used in the tdev function.  It is calculated from the
    constants d and b, and the scale exponent used in the pmNs function.  """
    return x('d')+0.2*(e()-x('b'))
  def pm():
    """pm is the person-month calculation, the amount of time one person spends 
    working on the project for one month.  It is calculated from the amount
    of effort in person-months, pmNs(), the measure of the schedule constraint 
    for the project, sced(), and the estimated effort, pmAuto()."""
    return pmNs()*x('sced')+pmAuto()
  def pmNs():
    """ pmNs is the amount of effort in person-months. pmNs is calculated from the 
    constant a(), size(), and the scale exponent, e(), and the following values. """
    return x('a') * (size()**e())*               \
        prod(x('rely','data','cplx','ruse',  
                     'docu','time','stor','pvol',
                     'acap','pcap','pcon','aexp','plex',
                     'ltex', 'tool', 'site'))    
  def pmAuto() :
   return (x('adaptedKsloc')*(x('at')/100))/x('atKProd') 
  def e() :
    """e is the scale exponent used in the pmNs function.  It calculated from
    the constant b and the percent result of summing the selected scale
    scale factors"""
    return x('b')+0.01*sum(x('prec','flex','resl','team','pmat'))
  #--- main
  months = pm()
  timE   = tdev()
  staff  = months/timE
  return months,timE,staff,it

def tunings( _ = None):
  return dict( 
    flex= [5.07, 4.05, 3.04, 2.03, 1.01,    _],
    pmat= [7.80, 6.24, 4.68, 3.12, 1.56,    _],
    prec= [6.20, 4.96, 3.72, 2.48, 1.24,    _],
    resl= [7.07, 5.65, 4.24, 2.83, 1.41,    _],
    team= [5.48, 4.38, 3.29, 2.19, 1.01,    _], 
    acap= [1.42, 1.19, 1.00, 0.85, 0.71,    _], 
    aexp= [1.22, 1.10, 1.00, 0.88, 0.81,    _], 
    cplx= [0.73, 0.87, 1.00, 1.17, 1.34, 1.74], 
    data= [   _, 0.90, 1.00, 1.14, 1.28,    _], 
    docu= [0.81, 0.91, 1.00, 1.11, 1.23,    _], 
    ltex= [1.20, 1.09, 1.00, 0.91, 0.84,    _], 
    pcap= [1.34, 1.15, 1.00, 0.88, 0.76,    _], 
    pcon= [1.29, 1.12, 1.00, 0.90, 0.81,    _], 
    plex= [1.19, 1.09, 1.00, 0.91, 0.85,    _], 
    pvol= [   _, 0.87, 1.00, 1.15, 1.30,    _], 
    rely= [0.82, 0.92, 1.00, 1.10, 1.26,    _], 
    ruse= [   _, 0.95, 1.00, 1.07, 1.15, 1.24], 
    sced= [1.43, 1.14, 1.00, 1.00, 1.00,    _], 
    site= [1.22, 1.09, 1.00, 0.93, 0.86, 0.80], 
    stor= [   _,    _, 1.00, 1.05, 1.17, 1.46], 
    time= [   _,    _, 1.00, 1.11, 1.29, 1.63], 
    tool= [1.17, 1.09, 1.00, 0.90, 0.78,    _])

months,timE,staff,it =  cocomo2000()

for k in sorted(it.keys()):
  print "%30s = %s" % (k,it[k].ask())
for k,v in (('-----------------------',
             '-----------------------'),
            ('months',months), ('timE',timE),('staff',staff)):
  print "%30s = %s" % (k,v)
