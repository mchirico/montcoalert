#!/usr/bin/env python
"""
  src: https://github.com/mchirico/montcoalert/raw/master/src/python/vomit.py

  You can run this on cloud9

    Install Anaconda:
      
      Step 1:

        Get the latest version of Anaconda2
         $ wget https://repo.continuum.io/archive/Anaconda2-2.5.0-Linux-x86_64.sh
         $ bash ./wget https://repo.continuum.io/archive/Anaconda2-2.5.0-Linux-x86_64.sh
  
  
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

# Read in the data
url="https://storage.googleapis.com/montco-stats/tz.csv"
d=requests.get(url).content
d=pd.read_csv(io.StringIO(d.decode('utf-8')))
d=pd.DataFrame(d)

# Set index
d.index = pd.DatetimeIndex(d.timeStamp)

# Take a look at just 'EMS: NAUSEA/VOMITING' for this year
# set to temporary variable tz
tz=d[(d.title == 'EMS: NAUSEA/VOMITING') & (d.timeStamp >= '2016-01-01 00:00:00')]

print tz.title.count()  # prints 187 currently

# Group by just title
g = d.groupby(['title'])

# Look at the data every 100 hours. Note 60T = 1hr, 60*100=6000
kt100=g['e'].resample('6000T', how=[np.sum,np.mean,np.median, len])
kt100.fillna(0, inplace=True)


# Write it out to .csv
vomit=kt100.ix['EMS: NAUSEA/VOMITING']['sum']
vomit.to_csv('vomit100hr.csv',index=True,header=True)

"""
  This is what we see in vomit100hr.csv
  ...
  2016-01-29 00:00:00,23.0
  2016-02-02 04:00:00,15.0
  2016-02-06 08:00:00,26.0
  2016-02-10 12:00:00,17.0
  
  Note that the last entry will almost always be a lower
  sum, since it doesn't contain the full 100hrs.
  
"""

# Let's look at every 50 hours... shorten the time
kt50=g['e'].resample('3000T', how=[np.sum,np.mean,np.median, len])
kt50.fillna(0, inplace=True)


# Write it out to .csv
vomit50=kt50.ix['EMS: NAUSEA/VOMITING']['sum']
vomit50.to_csv('vomit50hr.csv',index=True,header=True)
print vomit50.tail()
print "\n\nStats on 50hr"
print "Max: %d Mean:% 6.2f Median:% 6.2f" % (vomit50.max(),vomit50.mean(),vomit50.median())
s="Quantiles: 25%,   50%,  75%,   90%\n"
s+="         % 6.2f % 6.2f % 6.2f % 6.2f" % (vomit50.quantile(0.25),
                                             vomit50.quantile(0.50),
                                             vomit50.quantile(0.75),vomit50.quantile(0.9))
print s

#  If you want to see the display
#  vomit50.plot()
#  plt.savefig('vomit50.png', bbox_inches='tight')

"""
  Now we get the following
  ...
  2016-02-04 06:00:00,7.0
  2016-02-06 08:00:00,6.0
  2016-02-08 10:00:00,20.0   <---- A slight spike
  2016-02-10 12:00:00,13.0
  2016-02-12 14:00:00,4.0
  
  Stats on 50hr
  Max: 20 Mean:  8.31 Median:  7.00
  Quantiles: 25%,   50%,  75%,   90%
             6.00   7.00  10.00  13.00
  
  
"""


# Group by title and township
g = d.groupby(['title','twp'])

# Look at the data every 100 hours. Note 60T = 1hr, 60*100=6000
k100=g['e'].resample('6000T', how=[np.sum,np.mean,np.median, len])
k100.fillna(0, inplace=True)

# Create pivot table
# Start with the group we want
d.timeStamp=pd.DatetimeIndex(d.timeStamp)
tz=d[(d.title == 'EMS: NAUSEA/VOMITING')]

tz.index=pd.DatetimeIndex(tz.timeStamp)
#tz.index=pd.DatetimeIndex(tz.timeStamp)



p=pd.pivot_table(tz, values='e', index=['timeStamp'], columns=['twp'], aggfunc=np.sum)
#j=p.resample('4D',how='sum', fill_method='pad')
j=p.resample('72H',how='sum', fill_method='pad')
j.fillna(0, inplace=True)

j.index=j.index-pd.offsets.Hour(j.index.min().hour) - pd.offsets.Minute(j.index.min().minute) -pd.offsets.Second(j.index.min().second)
j.to_csv('vomitPivot.csv',index=True,header=True)

