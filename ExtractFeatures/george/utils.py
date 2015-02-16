INDEP = [ 
         # 0..8
         'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
         # 9 .. 17
         'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
         # 18 .. 25
         'ltex', 'tool', 'site', 'sced', 'kloc']

LESS = ['effort', 'defects', 'months']

DATATYPES = [int for x in range(22)] + [float for x in range(4)]
 
class ExtendedDataset:
  def __init__(i, dataset=None) :
    if (dataset == None) :
      i.dataset = set()
    else : 
      i.dataset = None
  def __len__(i):
    return len(i.dataset)
