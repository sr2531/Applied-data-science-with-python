import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties




url_ca = 'https://en.wikipedia.org/wiki/List_of_California_wildfires#cite_note-22'
url_usa = 'https://www.nifc.gov/fireInfo/nfn.htm'

df_ca = pd.read_html(url_ca,header =0)[4]
df_usa = pd.read_html(url_usa,header = 0)[0]


df_ca.drop(['Ref','Hectares'],axis = 1,inplace = True)
df_ca.drop(df_ca.tail(1).index,inplace = True)
df_ca.drop(df_ca.head(10).index,inplace = True)
df_ca.reset_index(drop = True,inplace = True)
row = ['2020','9639','4177856']
df_ca.loc[len(df_ca)] = row


df_ca
df_usa
df_ca.info()
df_usa.info()
df_usa.drop(df_usa.head(7).index,inplace =  True)
df_usa.drop(df_usa.tail(2).index,inplace =  True)
df_usa.reset_index(drop = True,inplace = True)
df_usa.columns = ['Year','US_Fires','US_Acres']



df_usa['Year'] = df_usa['Year'].str.split(" ").str[0]
df_usa['US_Fires'] = df_usa['US_Fires'].str.split(" ").str[1]
df_usa['US_Acres'] = df_usa['US_Acres'].str.split(" ").str[1]

df_ca['Fires'] = pd.to_numeric(df_ca['Fires'])
df_ca['Acres'] = pd.to_numeric(df_ca['Acres'])
df_usa.replace(',','',regex = True, inplace = True)
df_usa['US_Fires'] = pd.to_numeric(df_usa['US_Fires'])
df_usa['US_Acres'] = pd.to_numeric(df_usa['US_Acres'])

df_usa = df_usa.iloc[::-1]
df_usa.reset_index(drop = True,inplace = True)


df = pd.merge(df_ca,df_usa, on = 'Year')
df['Fire%'] = (df['Fires']/df['US_Fires'])*100
df['Acres%'] = (df['Acres']/df['US_Acres'])*100


fig = plt.figure(figsize = (10,5))
ax = fig.add_subplot(111) 
ax2 = ax.twinx()
width = 0.4
colors=['black','dimgray']

ax.set_ylabel('Fires')
ax2.set_ylabel('Acres')


rects1 = df.plot(x = 'Year', y = ['Fires','US_Fires'],kind='bar', ax=ax, width=width, position= 1, stacked = True,edgecolor='black')

rects2 = df.plot(x = 'Year', y = ['Acres','US_Acres'],kind='bar', ax=ax2, width=width, position= 0, stacked = True, color=colors,edgecolor='black')

ax.legend(['CA Fires','US Fires'], bbox_to_anchor=[0.65, 1], 
           loc=' upper center', ncol= 2, borderaxespad=0.05)

ax2.legend(['CA Acres','US Acres'], bbox_to_anchor=[0.35, 1.07], 
           loc=' upper center', ncol= 2, borderaxespad=0.05)



    
