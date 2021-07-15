#!/usr/bin/env python
# coding: utf-8

# <B>Import libraries

# In[75]:


import refinitiv.dataplatform.eikon as ek
import refinitiv.dataplatform as rdp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

ek.set_app_key('DEFAULT_CODE_BOOK_APP_KEY')
rdp.open_desktop_session('DEFAULT_CODE_BOOK_APP_KEY')


# <B>Define variable inputs

# In[7]:


companies = '0#.DJI' #can be changed to 0#.dMIWD00000PUS
start = '2016-06-01' 
end = '2021-07-01'
freq = 'D'


# <B>Retrieve universe of companies and their ESG scores, separate them into three tiers

# In[8]:


esgdata, err = ek.get_data(
    instruments = [companies],
    fields = ['TR.TRESGScore(Period=FY0).fperiod', 'TR.TRESGScore(Period=FY0)'],
    parameters = {'SDate' : start, 'Frq' : 'FY', 'EDate' : end}
    )

esgdata


# In[9]:


groupedesg = esgdata.groupby(['Instrument'])
topesgscore = groupedesg.max()
topesgscore = topesgscore.reset_index()
topesgscore


# In[10]:


topesgscore.dropna().head()


# In[11]:


sortedtopesgscore = topesgscore.sort_values(by='ESG Score',ascending=False)
cleanesgscores = sortedtopesgscore.dropna()
cleanesgscores.head()


# In[12]:


tier1, tier2, tier3 = np.array_split(cleanesgscores, 3)

tier1 = tier1.reset_index(drop=True)
tier1co = tier1.drop(columns=['ESG Score','Financial Period Absolute'])

tier1co


# In[13]:


tier2 = tier2.reset_index(drop=True)
tier2co = tier2.drop(columns=['ESG Score','Financial Period Absolute'])

tier2co


# In[14]:


tier3 = tier3.reset_index(drop=True)
tier3co = tier3.drop(columns=['ESG Score','Financial Period Absolute'])
tier3co


# <B>Retrieve daily market cap data for each tier and aggregate

# In[15]:


t1mktcapdata, err = ek.get_data(
    instruments = tier1co['Instrument'].tolist(),
    fields = ['TR.CompanyMarketCap.date', 'TR.CompanyMarketCap'],
    parameters = {'SDate' : start, 'Frq' : freq, 'EDate' : end,'RH':'IN'}
    )

t1mktcapdata


# In[37]:


t1dailymktcap = t1mktcapdata.groupby(['Date']).sum()
t1dailymktcap


# In[38]:


t2mktcapdata, err = ek.get_data(
    instruments = tier2co['Instrument'].tolist(),
    fields = ['TR.CompanyMarketCap.date', 'TR.CompanyMarketCap'],
    parameters = {'SDate' : start, 'Frq' : freq, 'EDate' : end,'RH':'IN'}
    )

t2mktcapdata


# In[40]:


t2dailymktcap = t2mktcapdata.groupby(['Date']).sum()
t2dailymktcap


# In[41]:


t3mktcapdata, err = ek.get_data(
    instruments = tier3co['Instrument'].tolist(),
    fields = ['TR.CompanyMarketCap.date', 'TR.CompanyMarketCap'],
    parameters = {'SDate' : start, 'Frq' : freq, 'EDate' : end,'RH':'IN'}
    )

t3mktcapdata


# In[42]:


t3dailymktcap = t3mktcapdata.groupby(['Date']).sum()
t3dailymktcap


# <B>Build chart

# In[66]:


t1dailymktcaprb = t1dailymktcap * 100 / (t1dailymktcap['Company Market Cap'][0])
t2dailymktcaprb = t2dailymktcap * 100 / (t2dailymktcap['Company Market Cap'][0])
t3dailymktcaprb = t3dailymktcap * 100 / (t3dailymktcap['Company Market Cap'][0])


# In[101]:


plt.figure(figsize=(10, 10))
plt.plot(t1dailymktcaprb, label= "Tier 1")
plt.plot(t2dailymktcaprb, label= "Tier 2")
plt.plot(t3dailymktcaprb, label= "Tier 3")
plt.xlabel('Date', fontsize=14)
plt.ylabel('Indexed Price Performance', fontsize=14)
plt.title('Decomposition of Returns by ESG Rating', fontsize=18)
plt.legend()
plt.show()


# In[ ]:




