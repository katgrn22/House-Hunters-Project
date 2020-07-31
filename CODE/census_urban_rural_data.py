
# coding: utf-8

# In[ ]:



import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import requests
import json


# In[ ]:


# Read recipe inputs
all_postal_codes_distinct_stacked = dataiku.Dataset("all_postal_codes_distinct_stacked")
all_postal_codes_distinct_stacked_df = all_postal_codes_distinct_stacked.get_dataframe()
df=all_postal_codes_distinct_stacked_df
print(len(df))
df.head()


# In[ ]:


#call urban/rural household api for each zip code

for i, row in df.iterrows():

    try:
        postal_code = str(df.PostalCode[i])

        url = 'https://api.census.gov/data/2010/dec/sf1?get=H001001,H002002,H002005&for=zip+code+tabulation+area:'+postal_code+'&key=2711068f602d3a9d09fc5e14ba20e194282e8592'
        print(url)

        r = requests.get(url)
        print(postal_code,": ",r.status_code)
        response_data = json.loads(r.text)

        if i == 0:
            print(i)
            df_out = pd.DataFrame(response_data[1:])
            print(len(df_out))
        else:
            #print(i)
            df_out = df_out.append(pd.DataFrame(response_data[1:]))
            print(len(df_out))

    except:
        print("except: ", postal_code)
        continue


# In[ ]:


df_out.head()


# In[ ]:


#add column names
df_out.rename(columns = {0:'TotalHouseholds',1:'UrbanHouseholds',2:'RuralHouseholds',3:'PostalCode'}, inplace = True)
df_out = df_out.reset_index(drop=True)
print(len(df_out))
df_out.head()


# In[ ]:


#write back to flow
census_urban_rural_data_df = df_out # For this sample code, simply copy input to output

# Write recipe outputs
census_urban_rural_data = dataiku.Dataset("census_urban_rural_data")
census_urban_rural_data.write_with_schema(census_urban_rural_data_df)

