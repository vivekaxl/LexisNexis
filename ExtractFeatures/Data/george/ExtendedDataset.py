class ExtendedDataset:
  def __init__(i, dataset=None) :
    if (dataset == None) :
      i.dataset = set()
    else :
      i.dataset = None
  def __len__(i):
    return len(i.dataset)

