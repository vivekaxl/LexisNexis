#reader.py

import io
import itertools
import operator
import tokenize
import sys
from math import sqrt

class Table(object):
  def __init__(i):
    i.header = []
    i.rows = []
    i.cols = []
    i.true = []
    i.false = []
    i.klass = ''

  def __str__(i):
    output = ''
    cnt=0
    while cnt < len(i.header):
      if i.cols[cnt].ignore == 0:
        if cnt == len(i.header)-1:
          output += str(i.header[cnt]) +' #\tnotes\n'
        else:
          output += str(i.header[cnt]) + ', '
      cnt+=1
    
    for col in i.cols:
      if col.ignore == 0:
        output += str(col.expected) + ', '
    output += '#\texpected\n'

    for col in i.cols:
      if col.ignore == 0:
        output += str(col.centroid) + ', '
    output += '#\tcertainty\n'

    cnt=0
    while cnt < len(i.rows):
      j=0
      while j < (len(i.cols)):
        if i.cols[j].ignore ==0:
          if (j == len(i.cols)-1):
            output += str(i.rows[cnt][j]) + '\t#\n'
          else:
            output += str(i.rows[cnt][j]) + ', '
        j+=1
      cnt+=1
    return output

  def addCol(i, name, Type, option=0):
    i.header.append(name)
    i.cols.append(Type)
    if option == 'klass':
      i.klass = Type
      i.true = Type.true
      i.false = Type.false

  def addRow(i, lst):
    i.rows.append(lst)

class Type(object):
  def __init__(i):
    i.data = []
    i.n = 0
    i.header = ''
    i.expected = ''
    i.centroid = 0.0

class Nump(Type):
  def __init__(i, option='default', ignore=0):
    super(Nump, i).__init__()
    i.mean = 0.0
    i.sd = 0.0
    i.option = option
    i.ignore = ignore

  def add(i, x):
    i.data.append(x)
    if (x != '?'):
      i.n+=1
      i.find_sd()
      i.expected = "{0:.2f}".format(i.mean)
      i.centroid = "{0:.2f}".format(i.sd)

  def find_sd(i):
    n=0
    delta=0.0
    mean=0.0
    m2=0.0
    for col in i.data:
      if (col != '?'):
        n+=1
        delta = float(col) - mean
        mean += delta/n
        i.mean = mean
        m2 += delta*(float(col)-mean)
    if i.n > 1:
      i.sd = sqrt(m2/(i.n-1))

class Wordp(Type):
  def __init__(i, option='default', ignore=0):
    super(Wordp, i).__init__()
    i.mode = 0.0
    i.modenum = 0
    i.option = option
    i.ignore = ignore   
    i.true = []
    i.false = []

  def add(i, x):
    i.data.append(x)
    i.n+=1
    i.find_expected(x)
    i.find_centroid()
    i.addIndex(x)

  def find_centroid(i):
    i.centroid = "{0:.2f}".format(i.modenum/float(i.n))

  def find_expected(i, x):
    if i.data.count(x) > i.modenum:
      i.modenum = i.data.count(x)
      i.mode = x
      i.expected = i.mode

  def addIndex(i, x):
    if x == 'yes':
      i.true.append(i.n)
    else:
      i.false.append(i.n)

# method pulled from stackoverflow discussion on removing comments
# link to discussion: http://goo.gl/13lRRA
def nocomment(s):
    result = []
    g = tokenize.generate_tokens(io.BytesIO(s).readline)  
    for toknum, tokval, _, _, _  in g:
        if toknum != tokenize.COMMENT:
            result.append((toknum, tokval))
    return tokenize.untokenize(result)

def reader(filename, lst=0):
  cnt = 0
  header = []
  with open(filename, 'rb') as f:
    for line in f:
      if line[0] == '#': continue
      string = nocomment(line).replace(' ', '').strip()
      if string.strip()[-1] == ',': header.append(string[:-1])
      elif cnt == 0:
        cnt+=1
        header.append(string)
        table = makeTable(header)
      else:
        if lst != 0:
          row_list=lst
          if cnt in row_list:
            temp = string.split(',')
            addRow(temp, table)
        else:
          temp = string.split(',')
          addRow(temp, table)
        cnt+=1
    return table

def makeTable(header):
  table = Table()
  for val in header:
    if val[0] == '?':
      if val[1] == '=':   table.addCol(val, Wordp('klass', 1), 'klass')
      elif val[1] == '+': table.addCol(val, Nump('max', 1))
      elif val[1] == '-': table.addCol(val, Nump('min', 1))
      elif val[1] == '$': table.addCol(val, Nump('default', 1))
      else:               table.addCol(val, Wordp('default', 1))
    elif val[0] == '=': table.addCol(val, Wordp('klass'), 'klass')
    elif val[0] == '+': table.addCol(val, Nump('max'))
    elif val[0] == '-': table.addCol(val, Nump('min'))
    elif val[0] == '$': table.addCol(val, Nump())
    else:               table.addCol(val, Wordp())
  return table

def addRow(temp,table):
  table.addRow(temp)
  cnt=0
  while cnt < len(temp):
    table.cols[cnt].add(temp[cnt])
    cnt+=1
