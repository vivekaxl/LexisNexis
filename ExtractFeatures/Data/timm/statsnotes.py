"""
<em>(Note to students: before you get scared about all this, note that I've coded
this up for you- see the demos in
[statsd.py](http://unbox.org/open/trunk/472/14/spring/var/code/statsd.html).
But you should not just use things
you do not understand. So read and enjoy.)</em>

Comparing Different Optimizers
=============================



For the most part, we are concerned with very
high-level issues that strike to the heart of the
human condition:

- What does it mean to find controlling principles in the world?
- How can we find those principles better, faster, cheaper?

But sometimes we have to leave those lofty heights
to discuss more pragmatic issues. Specifically, how
to present the results of an optimizer and,
sometimes, how to compare and rank the results from
different optimizers.

Note that there is no best way, and often the way we
present results depends on our goals, the data we
are procesing, and the audience we are trying to
reach.  So the statistical methods discussed below
are more like first-pass approximations to something
you may have to change extensively, depending on the
task at hand.

In any case, in order to have at least
one report that that you quickly generate, then....

Theory
------

The test that one optimizer is better than another can be recast
as four checks on the _distribution_ of performance scores. 

1. Visualize the data, somehow.
2. Check if the distributions are _significantly different_;
3. Check if the central tendency of one distribution is _better_ 
   than the other; e.g. compare their mean values.
4. Check the different between the central tendencies is not some _small effect_.

The first step is very important. Stats should
always be used as sanity checks on intuitions gained
by other means. So look at the data before making,
possibly bogus, inferences from it. For example,
here are some charts showing the effects on a
population as we apply more and more of some
treatment. Note that the mean of the populations
remains unchanged, yet we might still endorse the
treatment since it reduces the uncertainty
associated with each population.


<center>
<img width=300 
src="http://unbox.org/open/trunk/472/14/spring/doc/img/index_customers_clip_image002.jpg">
</center>


One possible bogus inference would be to apply the
third test without the second since if the second
_significance_ test fails, then the third _better_ test could give misleading results.  
For example, returning
to the above distributions, note  the large overlap
in the top two curves in those plots.  When
distributions exhibit a very large overlap, it is
very hard to determine if one is really different to
the other.  So large variances can mean that even if
the means are _better_, we cannot really say that
the values in one distribution are usually better
than the other.



Pragmatics
----------

There are several pragmatic issues associated with these tests.


### Experimental Design 

In a very famous quote, [Ernest Rutherford](http://en.wikipedia.org/wiki/Ernest_Rutherford) once said

+  _"If your experiment needs statistics, you ought to have done a better experiment_".

In this view, it is a mistake to perform arcane statistical tests on large sets
of results- far better to design your experiments better. 

In this subject,
we have seen one such paper that 
[explored multiple options in optimization](http://unbox.org/doc/pso/Off-The-Shelf_PSO.pdf)
but they did not explore all combinations. Rather, they walked through the space
of options comparing a few options at a time. 

While 
[that's a good paper](http://unbox.org/doc/pso/Off-The-Shelf_PSO.pdf), it does not explore
_interaction effects_ where some options, in combination with others, have unintended
side-effects. So all hail [Ernest Rutherford](http://en.wikipedia.org/wiki/Ernest_Rutherford)
but sometimes you just gotta look at many options.

So, on with the show.


### Effect size

Much recent commentary has
remarked that two sets of numbers can be
_significantly different_, but the size of that
difference is so small as to be very boring. For
example, the blue and red lines in the following are
significantly different:

<center>
<img width=300 
src="http://unbox.org/open/trunk/472/14/spring/doc/img/distributed.png">
</center>

But when you look at the _size_ of 
the difference, it is so small that you have
to say its kinda boring. The lesson here is that 
even if two distributions are _significantly difference_
and even if their means are _better_, then if the _effect size_
is very small then we should not report a difference in the population.

In the following, we will use the _a12_ test for effect size.


### Handling Distributions of Many Shapes

Data may be _shaped_ in funny ways. Consider the following
distributions:

<center>
<img width=400 
src="http://unbox.org/open/trunk/472/14/spring/doc/img/dists.gif">
</center>

Note that  these are all not smooth symmetrical bell-shaped curves
that rise to a single maximum value. Why is this important? Well, several
of the widely used tests of _statistical significance_ assume such shapes.
One method that does not is the _bootstrap sampling_ method discussed below- but
that requires hundreds to thousands of resamples of the domain (which can be
slow for very large distributions). So, pragmatically, if we want to avoid
assuming that the data fits some particular shape then we need to somehow
restrict the number of times we apply slower methods like bootstrapping.


Note that one reason we use the _a12_ test for effect size is that
this particular test makes no assumptions about the shape of the data being explored.

Note also that bootstrapping can be very, very slow indeed. A constant plea
in the bootstrapping literature is "tell us how to make it run faster".
In the following, we will minimize the calls to bootstrapping as follows:

+ Only bootstrap if the effect size is not small;

That is, instead of checking for effect size _after_ checking for _significant difference_,
we check _before_. This is important since it avoid unnecessary calls (and very slow)
calls to bootstrapping.

### The Confidence Problem

A second pragmatic issue is the _confidence_
issue. Suppose we have four optimizers, each of
which is controlled by four parameters
(e.g. mutation rate etc), and you are testing these
on 10 models (Fonseca, ZDT, etc). If you break the
parameters into (say) three big chunks (e.g. lo,
medium, high), in effect you are comparing results
on 10*4*3<sup>4</sup>=3,240 _treatments_; i.e. over
5,000,000 comparisons.  Now it is sensible to
explore treatments within each model separately, which means you are
"only" comparing pairs of 324 numbers, which is
still over 50,000 comparisons.

Why is this a problem? Well, tests for
_significantly difference_ report the probability
that members of population1 do not overlap
population2. In practice, most populations overlap a
little, so standard practice is to restrict the
overlap test to some small number; e.g. report that
two populations are significantly different if 95%
of the members are not found in the overlap.

Now can you see the problem? If these tests are 95% confident
and we run 324 such comparisons tests, our results
now have confidence 0.95<sup>50,000</sup>=0.0000061%
confident (i.e. not confident at all.

An alternative to the above is to sort all the
results from different treatments on their mean value,
then compare the optimizer at position _i_ to position
_i+1_. 
Note that this procedure requires _N-1_ comparisons
for _N_ treatments.
So now for 324 treatments, our statistical tests are
confident to 0.95<sup>323</sup>=0.000006 percent- which
is better than before but still very very very poor.

Yet another alternative is to sort the data then
conduct a binary chop on the results, and only run
the significance tests on each chop.  For our 323
treatments, this will generate results with
a confidence of   0.95<sup>log2(323)</sup>=65%.

This can be improved further but only chopping the
data at points where the mean value of the
treatments in each chop are most different.  This is
the _Scott-Knott_ procedure discussed below.  If
some population has mean _mu_ and some chop divides
the _n_ members of that population into _n1_ and
_n2_ groups with means _mu1_ and _mu2_, then the
expected value of the difference the mean before and
after the chop is:
 
     delta = n1/n*(mu - mu1)**2 + n2/n*(mu - mu2)**2  

Scott-Knott picks the chops that  maximizes _delta_.
In the code shown below, that Scott-Knott also rejects chops
that:

- Generate tiny groups in the data- e.g. less than 4 individuals in any chop;
- Are different by only some _small effect_ implemented using, say,  the _a12_ test discussed below.

As mentioned above, this second step (running _a12_ before checking for significant differences)
is a way to reduce the time required for bootstrapping.

More importantly, the fewer chops we explore, the fewer times we run
bootstrap and the fewer times we run into the confidence problem.
Just as a "what-if", support our Scott-Knott means we only
have to chop the data 20 times (which is actually more that usual).
If so, the our confidence in the conclusions would be 0.95<sup>log2(20)</sup> which is
80 percent- which is not bad for a study looking at 324 options.


Enough theory, on with the code


## How to...

### Visualization


As said above, stats should
always be used as sanity checks on intuitions gained
by other means.  


Suppose we had two optimizers which in a 10 repeated
runs generated performance from two models:

"""
    def _tile2():
      def show(lst):
         return xtile(lst,lo=0, hi=1,width=25,
                      show= lambda s:" %3.2f" % s)
      print "one", show([0.21, 0.29, 0.28, 0.32, 0.32, 
                         0.28, 0.29, 0.41, 0.42, 0.48])
      print "two", show([0.71, 0.92, 0.80, 0.79, 0.78, 
                         0.9,  0.71, 0.82, 0.79, 0.98])
"""

When faced with new data, always chant the following mantra:

+ _First_ visualize it to get some intuitions;
+ _Then_ apply some statistics to double check those intuitions.

That is, it is _strong recommended_ that, prior
doing any statistical work, an analyst generates a
visualization of the data. Percentile charts a
simple way to display very large populations in very
little space. For example, here are our results from
_one_, displayed on a range from 0.00 to 1.00.

    one         * --|            , 0.28,  0.29,  0.32,  0.41,  0.48
    two             |    -- * -- , 0.71,  0.79,  0.80,  0.90,  0.98

In this percentile chart, the 2nd and 3rd
percentiles as little dashes left and right of the
median value, shown with a _"*"_, (learner _two_'s
3rd percentile is so small that it actually
disappears in this display).  The vertical bar _"|"_
shows half way between the display's min and max (in
this case, that would be (0.0+1.00)/2= 0.50)

From the above, we could write a little report that
shows the mean and rank performance of the two
learners.

    one  :mu 0.32 :rank 1
    two  :mu 0.80 :rank 2

From this report, if the goal was to maximize some
factor, then it is clear we would recommend _two_
over optimizer__one_.

#### Xtile

The advantage of percentile charts is that we can
show a lot of data in very little space. For
example, here's 2000 numbers shown as a _quintile_
chart on two lines.

+ Quintiles divide the data into the 10th, 30th,
  50th, 70th, 90th percentile.
+ Dashes (_"-"_) mark the range (10,30)th and
  (70,90)th percentiles;
+ White space marks the ranges (30,50)th and
  (50,70)th percentiles.

Consider two distributions, of 1000 samples each:
one shows square root of a _rand()_ and the other
shows the square of a _rand()_.
"""

    def _tile() :
      import random
      r = random.random
      def show(lst):
        return xtile(lst,lo=0, hi=1,width=25,
                     show= lambda s:" %3.2f" % s)
      print "one", show([r()**0.5 for x in range(1000)])
      print "two", show([r()**2   for x in range(1000)])

"""

In the following quintile  charts, we show these distributions:

+ The range is 0 to 1.
+ One line shows the square of 1000 random numbers;
+ The other line shows the square root of 1000 random numbers;
  
Note the brevity of the display:
	
	one        -----|    *  ---  , 0.32,  0.55,  0.70,  0.84,  0.95
    two --    *     |--------    , 0.01,  0.10,  0.27,  0.51,  0.85

As before, the median value, shown with a _"*"_; and
the point half-way between min and max (in this
case, 0.5) is shown as a vertical bar _"|"_.

For details on how to draw percentile charts, _xtiles_
in [do.py](http://unbox.org/open/trunk/472/14/spring/var/code/do.html)


### The Scott-Knott Procedure


Suppose we have four optimizers which have been run
four times each, there is more wriggle in their
results:

    one   0.34 0.49 0.51  0.8
    two   0.6  0.9  0.8   0.9
    three 0.7  0.9  0.8   0.6
    four  0.2  0.3  0.35  0.4

To rank these, we'd first sort them by their mean
and maybe add a little bar chart to the

    four  :mu 0.3125   ******
    one   :mu 0.535    ***********
    three :mu 0.75     ***************
    two   :mu 0.8      ****************

Intuitively, the learners seem to fall into three groups:

+ Highest scores: two and three;
+ Lowest scores: four;
+ Somewhere in-between: one.

The problem though is that it is a little hard to
check if those are the right groups since some of
these learners generate numbers very close to each
other.

Just as an aside, part of the problem is
insufficient experimentation. Four runs barely
exercises the optimizers so it does not given any of
them a chance to show their true worth. I recommend
at 10 to 20 repeats- but then another problem
arises; i.e. too many numbers to read and
understand.

If we explore the above using a _Scott-Knott_
procedure, then we would:

+ Sort the learners by their mean (as above)
+ Recursively _cut_ the list in two, stopping when 
  one half of the cut was similar
  to the other half. 
+ <em>Scott AJ and Knott M (1974) Cluster analysis method for
   grouping means in the analysis of variance. Biometrics 30:
   507-512.</em>
  
There any many ways to find the _cut_. Following the
recommendations of Mittas and Angelis, we proceed as
follows.

+  <em>Nikolaos Mittas, Lefteris Angelis: Ranking and Clustering Software Cost Estimation 
   Models through a Multiple Comparisons Algorithm. IEEE Trans. Software Eng. 39(4): 537-551 (2013)</em>

Mittas and Angelsis find the cut by collecting:

+ The mean `mu` of all the data below the cut;
+ The mean `mu0,mu1` of all the data below,above the cut.
+ Then return the cut that   most divides the data.

More specifically, according to Mittas and
 Angelesis, the best cut is the one that _maximizes
 the difference in the mean_ before and after the
 cut.
"""

    def minMu(parts,all,big,same):
      cut,left,right = None,None,None
      before, mu     =  0, all.mu
      for i,l,r in leftRight(parts):
        if big(l.n) and big(r.n): 
          if not same(l,r):
            n = all.n * 1.0
            x = l.n/n*(mu - l.mu)**2 + \
			    r.n/n*(mu - r.mu)**2  
            if x > before:
              before,cut,left,right = x,i,l,r
      return cut,left,right
"""

In the above _l.n_ and _r.n_ are the number of
measurements left and right of the cut (and _n_ =
_l.n + r.n_). So the above function gives most
weight to larger cuts that most change the mean of
the most number of measurements.

The _minMu_ function is a low-level procedure. A higher-level
tool calls _minMu_ to find one cut, then recurses on each cut.

"""

    def rdiv(data,  # a list of class Nums
             all,   # all the data combined into one num
             div,   # function: find the best split
             big,   # function: rejects small splits
             same): # function: rejects similar splits
      def recurse(parts,all,rank=0):
        cut,left,right = div(parts,all,big,same)
        if cut: 
          # if cut, rank "right" higher than "left"
          rank = recurse(parts[:cut],left,rank) + 1
          rank = recurse(parts[cut:],right,rank)
        else: 
          # if no cut, then all get same rank
          for part in parts: 
            part.rank = rank
        return rank
      recurse(sorted(data),all)
      return data
"""
Finally, the above is called by _scottknott_ that
recursively splits data, maximizing delta of the
expected value of the mean before and after the
splits (and rejects splits with under 3 items).

"""
    def scottknott(data,small=3,b=250, conf=0.05):
      def theSame(one, two):
        if a12small(two, one): return True
        return  not bootstrap(one, two, b=b, conf=conf)
      all  = reduce(lambda x,y:x+y,data)
      same = lambda l,r: theSame(l.saw(), r.saw())
      big  = lambda    n: n > small    
      return rdiv(data,all,minMu,big,same)

"""

(The _a12small_ and _bootstrap_ functions will be
explained below).


When this is run on the following data from
"_x1,x2,x3,x4,x5_" we see sensible groupings:

"""
    def rdivDemo(data):
      data = map(lambda lst:Num(lst[0],lst[1:],keep=512),
                 data)
      for x in sorted(scottknott(data),key=lambda y:y.rank):
        print x.rank, x.name, gs([x.mu, x.s])
    
    def rdiv2():
      rdivDemo([
            ["x1",0.34, 0.49, 0.51, 0.6],
            ["x2",0.6,  0.7,  0.8,  0.9],
            ["x3",0.15, 0.25, 0.4,  0.35],
            ["x4",0.6,  0.7,  0.8,  0.9],
            ["x5",0.1,  0.2,  0.3,  0.4]
            ])
"""

Note that `rdiv` performs a binary chop on the list
of optimizers. This is important since it means we
can rank _N_ learners using _log2(N)_
comparisons. This is very important, for reasons
we'll see shortly.

For full details on the Scott-Knott procedure, see
[stats.py](http://unbox.org/open/trunk/472/14/spring/var/code/stats.html).


### The A12 test


I prefer a test for _small effect_ that has does not
_sweat the small stuff_; i.e. ignore small
differences between items in the samples. My
preferred test for _small effect_ has:

+ a simple intuition;
+ which makes no assumptions about (say) Gaussian
  assumptions;
+ and which has a solid lineage in the literature.  

Such a test is Vargha and Delaney's _A12 statistic_-
The stastic was proposed in Vargha and Delaney's
2000 paper was endorsed in many places including in
Acruci and Briad's ICSE 2011 paper.

+ <em>A. Vargha and H. D. Delaney. A critique and
  improvement of the CL common language effect size
  statistics of McGraw and Wong. Journal of
  Educational and Behavioral Statistics,
  25(2):101-132, 2000
+ Andrea Arcuri, Lionel C. Briand: A practical guide
  for using statistical tests to assess randomized
  algorithms in software engineering. ICSE 2011:
  1-10</em>

After I describe it to you, you will wonder why
anyone would ever want to use anything else.  Given
a performance measure seen in _m_ measures of _X_
and _n_ measures of _Y_, the A12 statistics measures
the probability that running algorithm _X_ yields
higher values than running another algorithm _Y_.
Specifically, it counts how often we seen larger
numbers in _X_ than _Y_ (and if the same numbers
are found in both, we add a half mark):

     a12= #(X.i > Y.j) / (n*m) + .5#(X.i == Y.j) / (n*m)

According to Vargha and Delaney, a small, medium, large difference
between two populations is:

+ _large_ if `a12` is over 71%;
+ _medium_ if `a12` is over 64%;
+ _small_ if `a12` is  56%, or less.

The code is very simple- just remember to sort _lst1_ and
_lst2_ before doing the comparisons:

"""
    def a12small(lst1, lst2): return a12(lst1,lst2) <= 0.56
	
    def a12(lst1,lst2, gt= lambda x,y: x > y):
      "how often is x in lst1 more than y in lst2?"
      def loop(t,t1,t2): 
        while t1.i < t1.n and t2.i < t2.n:
          h1 = t1.l[t1.i]
          h2 = t2.l[t2.i]
          if gt(h1,h2):
            t1.i  += 1; t1.gt += t2.n - t2.i
          elif h1 == h2:
            t2.i  += 1; t1.eq += 1; t2.eq += 1
          else:
            t2,t1  = t1,t2
        return t.gt*1.0, t.eq*1.0
      #--------------------------
      lst1 = sorted(lst1, cmp=gt)
      lst2 = sorted(lst2, cmp=gt)
      n1   = len(lst1)
      n2   = len(lst2)
      t1   = Thing(l=lst1,i=0,eq=0,gt=0,n=n1)
      t2   = Thing(l=lst2,i=0,eq=0,gt=0,n=n2)
      gt,eq= loop(t1, t1, t2)
      return gt/(n1*n2) + eq/2/(n1*n2)
 
"""
### Bootstrap Tests

(_For more details on this section, see  p220 to 223 of Efron's book "An introduction to the bootstrap"._)


Formally, _a12_ is actually a _post hoc effect size
test_, which is applied _after_ some hypothesis test
for statistically significant difference between two
populations.

Such statistical tests check if there is enough of a
difference between two lists of numbers to falsify
some hypothesis (e.g. the values in list1 are less than
those in list2). Usual practice is to make some
parametric  assumption (e.g. that the numbers come
from a Gaussian distribution). 

Another method is called _bootstrapping_ that makes
no parametric assumption. The way it works is to
define some _testStatistic_ and apply it to:

1. The original two lists; 
2. A "bootstrap" sample;
   i.e. two artificially created lists created by
   sampling with replacement from the original lists.
  
A bootstrap test runs the _testStatistic_:

+ Once on the original pair of lists...
+ Then (say) 1000 times on 1000 bootstrap samples.

Then we return how often in the bootstrap samples,
the _testStatistic_ returns the same value as with
the original list (see the last line of the following code):

"""
    def bootstrap(y0,z0,conf=0.05,b=1000):
      class total():
        def __init__(i,some=[]):
          i.sum = i.n = i.mu = 0 ; i.all=[]
          for one in some: i.put(one)
        def put(i,x):
          i.all.append(x);
          i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
        def __add__(i1,i2): return total(i1.all + i2.all)
      def testStatistic(y,z): 
        tmp1 = tmp2 = 0
        for y1 in y.all: tmp1 += (y1 - y.mu)**2 
        for z1 in z.all: tmp2 += (z1 - z.mu)**2
        s1    = float(tmp1)/(y.n - 1)
        s2    = float(tmp2)/(z.n - 1)
        delta = z.mu - y.mu
        if s1+s2:
          delta =  delta/((s1/y.n + s2/z.n)**0.5)
        return delta
      def one(lst): return lst[ int(any(len(lst))) ]
      def any(n)  : return random.uniform(0,n)
      y, z   = total(y0), total(z0)
      x      = y + z
      tobs   = testStatistic(y,z)
      yhat   = [y1 - y.mu + x.mu for y1 in y.all]
      zhat   = [z1 - z.mu + x.mu for z1 in z.all]
      bigger = 0.0
      for i in range(b):
        if testStatistic(total([one(yhat) for _ in yhat]),
                         total([one(zhat) for _ in zhat])) > tobs:
          bigger += 1
      return bigger / b < conf
"""

In the above, the bootstrap sample is generated with the call the _one_.
This data is collected and summarized with the _total_ class.
Also, the _testStatsitic_ function
   checks if two means are different, tempered
         by the size of the two lists and the variance of the data.
   
One issue with the above is the number of
bootstrap. There are some statistical results that
say 200 to 300 bootstrap samples are enough. Note
that the more bootstrap samples, the slower the
statistical test (which is why folks often use the
faster parametric methods- even if the parametric 
methods make the wrong assumptions about the data).

For this reason,  this code  runs _bootstrap_
within a Scott-Knott that calls it only on "interesting" chops
(i.e. those that are not too small, that divide the data on more than a small
effect, and that maximize the expected value of the delta of the mean).

## Demos

All the above is coded up.
See [statsd.py](http://unbox.org/open/trunk/472/14/spring/var/code/statsd.html).
Share and enjoy.

"""
