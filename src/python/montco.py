#!/usr/bin/env python
"""
  This reads in data from montco. This reads it in as
  soon as you load it. Why? Because I didn't want to create
  the extra step.

     d=montco.d

  Common commands:
     reload(montco)

     g = d.groupby(['title'])
     g.sum()

     # Use loc to locate a specific index
     d.loc[(d['timeStamp'] >= '2016-03-20') & ( d['timeStamp'] <= '2016-04-07'       ),'train_id'].head()



Example that works:

     d.index = pd.DatetimeIndex(d.timeStamp)
     g = d.groupby([pd.TimeGrouper('1D'), 'title'])
     g['title'].count()
     gg=g['title'].count().unstack().fillna(0)

     r=gg.reset_index()
     r=r.rename(columns = {'index':'date'})


#     gg=pd.DataFrame(g.sum().to_records())
     gg=g.sum().reset_index()
     
     tlist=gg[(gg.e > myRange)].sort_values(by='e')['title'].tolist()

     d.index = pd.DatetimeIndex(d.timeStamp)
     df.to_csv('df.csv',index=True,header=True)

     df['datetime'].apply(lambda x: x.strftime('%d%m%Y'))
     r['hr']=r['timeStamp'].apply(lambda x: x.strftime('%H'))
     r['hr']=r['hr'].apply(lambda x: int(x))

  Resample

     d.index = pd.DatetimeIndex(d.timeStamp)
     t=d[d.title.str.match(r'EMS.*')]
     k=d[['title','e']].resample('3000T', how=[np.sum,np.mean,np.median, len])

  
     d..fillna(0, inplace=True)
   
  Flatten  z

     [item for sublist in z for item in sublist]


  def fcl(df, dtObj):
    return df.iloc[np.argmin(np.abs(df.index.to_pydatetime() - dtObj))]
  e=e.rename(columns = {'desc':'desc_orig'})
  e['d']=e.index.to_pydatetime()
  e['desc']=e['d'].apply(lambda x: fcl(t,x)['desc'])


  Interesting:

     >>> Series(['a', 'b', 'c']).str.cat(['A', 'B', 'C'], sep=',')
     0    a,A
     1    b,B
     2    c,C

     >>> Series(['a', 'b', 'c']).str.cat(sep=',')
     'a,b,c'

     >>> Series(['a', 'b']).str.cat([['x', 'y'], ['1', '2']], sep=',')
     0    a,x,1
     1    b,y,2

     >>> Series(['a1', 'b2', 'c3']).str.extract('(?P<letter>[ab])(?P<digit>\d)')
         letter digit
      0      a     1
      1      b     2
      2    NaN   NaN


 |  get_dummies(self, sep='|')
 |      Split each string in the Series by sep and return a frame of
 |      dummy/indicator variables.
 |
 |      Parameters
 |      ----------
 |      sep : string, default "|"
 |          String to split on.
 |
 |      Returns
 |      -------
 |      dummies : DataFrame
 |
 |      Examples
 |      --------
 |      >>> Series(['a|b', 'a', 'a|c']).str.get_dummies()
 |         a  b  c
 |      0  1  1  0
 |      1  1  0  0
 |      2  1  0  1

   t=d[d.desc.str.match(r'.*RT309.*') & d.title.str.match(r'.*VEHICLE ACCIDENT.*')]
   t=t[t.twp == 'UPPER DUBLIN']

   t=d[d.desc.str.match(r'.**') & d.title.str.match(r'.*VEHICLE ACCIDENT.*')]
   t=t[t.twp == 'UPPER DUBLIN']

   t=d[d.desc.str.match(r'.*ASHBOURNE RD & PARK AVE.*') & d.twp.str.match(r'.*CHELTENHAM.*')]
   t=t[t['timeStamp'] > '2016-01-01']
   g=t.groupby(['title'])
   g.sum()



CHELTENHAM:

   p=montco.readCR()
   d=montco.d

   p.index = pd.DatetimeIndex(p.timeStamp)
   c=p[(p.dtype == 'Traffic')]
   c['d']=c.index.to_pydatetime()

   m=d[(d.title == 'Traffic: VEHICLE ACCIDENT -') & (d.twp == 'CHELTENHAM')] 

def fcl(df, dtObj):
    return df.iloc[np.argmin(np.abs(df.index.to_pydatetime() - dtObj))]

import numpy as np

    c['daddr']=c['d'].apply(lambda x: fcl(m,x)['desc'])
    c['dd']=c['d'].apply(lambda x: fcl(m,x)['timeStamp'])
    
    c['dd']=c['dd'].apply(lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))
    c['delta']=c['dd']-c['d']
    c.to_csv('/Users/mchirico/c.csv',index=True,header=True)

    p.to_csv('/Users/mchirico/p.csv',index=True,header=True)


Quick:

   gg.sort_values(by='e',inplace=True)
   date=now() - datetime.timedelta(days=7)






"""
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



# Working on mce site
from pytz import timezone
import pytz
eastern = timezone('US/Eastern')
import time
# now().strftime('%Y-%m-%d %H:%M:%S')
def nowf():
    return now().strftime('%Y-%m-%d %H:%M:%S')
def nowfd():
    return now().strftime('%Y-%m-%d 00:00:00')
def now():
    timezone='US/Eastern'
    native=datetime.datetime.now()
    if time.timezone == 0:
        return native.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))
    else:
        return native



# Reading in data
import requests
requests.packages.urllib3.disable_warnings()


import pandas as pd
import io
import datetime


def readE():
    url="https://storage.googleapis.com/montco-stats/eslu.csv"
    d=requests.get(url,verify=False).content
    d=pd.read_csv(io.StringIO(d.decode('utf-8')),
                  header=0,names=['eid', 'id','type','station','loc','mun','date','time','unit','status'],
            dtype={'eid':str,'id':str,'type':str,'station':str,'loc':str,
                   'mun':str,'date':str,'time':str,'unit':str,'status':str})
    d=pd.DataFrame(d)
    d['eid']=d['eid'].apply(lambda x: x.replace('eid=',''))
    d['id']=d['id'].apply(lambda x: x.replace('incidentno=',''))
    d['type']=d['type'].apply(lambda x: x.replace('incidenttype=',''))
    d['loc']=d['loc'].apply(lambda x: x.replace('location=',''))
    d['mun']=d['mun'].apply(lambda x: x.replace('mun=',''))
    d['station']=d['station'].apply(lambda x: x.replace('station=',''))
    d.timeStamp=pd.DatetimeIndex(d.date+' '+d.time)
    d.index = d.timeStamp

    return d


# Read in the data
def readCR():
    url="https://storage.googleapis.com/montco-stats/cheltenham/cheltenhamCR2016.csv"
    d=requests.get(url,verify=False).content
    d=pd.read_csv(io.StringIO(d.decode('utf-8')),
                  header=0,names=['dtype','timeStamp','addr','id','desc','agency','lat','lng'],
            dtype={'dtype':str,'timeStamp':str,'addr':str,'id':str,
                   'desc':str,'agency':str,'lat':str,'lng':str})
    d=pd.DataFrame(d)
    d.timeStamp=d['timeStamp'].apply(lambda x: datetime.datetime.strptime(x,'%m/%d/%y %H:%M'))
    d.index = pd.DatetimeIndex(d.timeStamp)
    d['e']=1
    return d




# Read in the data
def readTZ():
    url="https://storage.googleapis.com/montco-stats/tz.csv"
    d=requests.get(url,verify=False).content
    d=pd.read_csv(io.StringIO(d.decode('utf-8')),
                  header=0,names=['lat', 'lng','desc','zip','title','timeStamp','twp','e'],
            dtype={'lat':str,'lng':str,'desc':str,'zip':str,
                  'title':str,'timeStamp':datetime.datetime,'twp':str,'e':int})
    d=pd.DataFrame(d)
    return d

d=readTZ()
d.index = pd.DatetimeIndex(d.timeStamp)

def gg(d=d,title='title'):
    date=datetime.datetime.now() - datetime.timedelta(days=7)
    date=date.strftime('%Y-%m-%d 00:00:00')
    c=d[d.timeStamp >= date]
    g=c.groupby(title)
    gg=g.sum().reset_index()
    gg.sort_values(by='e',inplace=True,ascending=[0])
    return gg

def ggc(d=d,title='title'):
    date=datetime.datetime.now() - datetime.timedelta(days=7)
    date=date.strftime('%Y-%m-%d 00:00:00')
    c=d[(d.timeStamp >= date) & (d.twp == 'CHELTENHAM')]
    g=c.groupby(title)
    gg=g.sum().reset_index()
    gg.sort_values(by='e',inplace=True,ascending=[0])
    return gg
