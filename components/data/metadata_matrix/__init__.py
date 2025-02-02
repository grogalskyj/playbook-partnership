import re
import contextlib
import fsspec
import numpy as np
import pandas as pd

@contextlib.contextmanager
def fsspec_open_as_iterator(url, *args, **kwargs) -> str:
  with fsspec.open(url, *args, **kwargs) as fr:
    yield fr

@contextlib.contextmanager
def fsspec_open_as_path(url, *args, **kwargs) -> str:
  m = re.match(r'^file://(.+)$', url)
  assert m, 'protocol not yet supported'
  yield m.group(1)

def metadata_from_path(path):
  ''' Read from a bunch of different formats, get a metadata table
  '''
  if path.endswith('.csv'):
    with fsspec_open_as_iterator(path, 'r') as fr:
      return pd.read_csv(fr, index_col=0)
  elif path.endswith('.tsv'):
    with fsspec_open_as_iterator(path, 'r') as fr:
      return pd.read_csv(fr, sep='\t', index_col=0)
  elif path.endswith('.txt') or path.endswith('.tab') or path.endswith('.data'):
    with fsspec_open_as_iterator(path, 'r') as fr:
      return pd.read_csv(fr, sep=None, index_col=0, engine='python')
  elif path.endswith('.xlsx'):
    with fsspec_open_as_path(path, 'r') as fr:
      return pd.read_excel(fr, index_col=0)
  else:
    raise NotImplementedError

def np_jsonifyable(x):
  x_ = x.astype('object')
  return x_.tolist()

def metadata_matrix(url):
  ''' Read the metadata file
  '''
  d = metadata_from_path(url)
  if d.shape[0] >= 10:
    top = 5
    bottom = 5
  elif d.shape[0] > 5:
    top = 5
    bottom = d.shape[0] - top
  else:
    top = d.shape[0] - 1
    bottom = 1

  if d.shape[1] != 1: 
    raise Exception("Metadata file should contain exactly one column \
                    indicating the class to which each sample belongs.")
  col = d.columns[0]
  if len(d[col].unique()) != 2: 
    raise Exception("Sample class column should only have two unique values, \
                    identifying the control group and perturbation group.")

  index = np.concatenate([d.index[:top], d.index[-bottom:]]).tolist()
  columns = d.columns.tolist()
  values = np_jsonifyable(np.concatenate([
    d.iloc[:top], d.iloc[-bottom:]
  ]))
  ellipses = [
    top if len(index) != d.shape[0] else None, 
    None,
  ]
  return dict(
    url=url,
    shape=d.shape,
    index=index,
    columns=columns,
    values=values,
    ellipses=ellipses,
  )
