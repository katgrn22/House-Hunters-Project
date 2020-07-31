
# coding: utf-8

# In[ ]:


get_ipython().magic(u'pylab inline')


# In[ ]:


import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import requests
import json


# In[ ]:


# Example: load a DSS dataset as a Pandas dataframe
#mydataset = dataiku.Dataset("mydataset")
#mydataset_df = mydataset.get_dataframe()


# In[ ]:


#get api key from parameter
api_key = '84f7accb1a71f34a44559380503efa9d'


# In[ ]:


#make api call
#100 properties returned per call. For 300,000 properties, will need 3,000 calls
#top max = 100; skip max = 10,000
#use PropType 'Residential' and 'Multi-Family' to limit calls
#use LivingArea to limit calls

#Residential

#LivingArea buckets. Need to limit each set of calls to 10K
#buckets = ['250','1000','1250','1400','1550','1650','1750','1850','1950','2050','2150','2250','2400','2550','2700','2850','3000','3150','3400','3900','10000']
buckets = ['250','1000','1250','1400']

for i in range(len(buckets[:-1])):
    try:
        for c in range(0,101):
            call = str(c*100)
            url = "http://api.bridgedataoutput.com/api/v2/OData/abor_ref/Property?access_token="+api_key+"&$skip="+call+"&$top=100&$filter=PropertyType%20eq%20%27Residential%27%20and%20LivingArea%20ge%20"+buckets[i]+"%20and%20LivingArea%20lt%20"+buckets[i+1]
            print(url)

            r = requests.get(url)
            print(c,": ",r.status_code)
            response_data = json.loads(r.text)

            if i == 0 and c == 0:
                print(i)
                df = pd.DataFrame.from_dict(response_data['value'])
                print(len(df))
            else:
                df = df.append(pd.DataFrame.from_dict(response_data['value']))
                print(len(df))
    except:
        print("except")
        continue


# In[ ]:


#len(df)


# In[ ]:


# Recipe outputs
austin_data = dataiku.Dataset("austin_data")
austin_data.write_with_schema(df)

