import pandas as pd
import matplotlib as mpl
mpl.get_backend()
import matplotlib.pyplot as plt
import  numpy as np
df = pd.read_csv("data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv. ")

df

df.info()
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.strftime('%m-%d')
df['Month'] = pd.DatetimeIndex(df['Date']).month
df['Year'] = pd.DatetimeIndex(df['Date']).year
df = df[df['Day'] != '02-29']


test = '2014-12-31'
cut_off = pd.to_datetime(test)
df1 = df[df['Date']<= cut_off]
df2 = df[df['Date']> cut_off]

mx = df1[df1['Element'] == 'TMAX'].groupby(['Day'])['Data_Value'].max().reset_index()
mx.set_index('Day',inplace = True)

mn = df1[df1['Element'] == 'TMIN'].groupby(['Day'])['Data_Value'].min().reset_index()
mn.set_index('Day',inplace = True)

mx_2015 = df2[df2['Element'] == 'TMAX'].groupby(['Day'])['Data_Value'].max().reset_index()
mx_2015.set_index('Day',inplace = True)
mn_2015 = df2[df2['Element'] == 'TMIN'].groupby(['Day'])['Data_Value'].min().reset_index()
mn_2015.set_index('Day',inplace = True)


data = pd.merge(mx, mn, left_index=True, right_index=True)

data.rename(columns ={'Data_Value_x':'Max_temp','Data_Value_y':'Min_temp'},inplace = True)

data2015 = pd.merge(mx_2015, mn_2015, left_index=True, right_index=True)

data.rename(columns ={'Data_Value_x':'Max_temp','Data_Value_y':'Min_temp'},inplace = True)
data2015.rename(columns ={'Data_Value_x':'Max_temp','Data_Value_y':'Min_temp'},inplace = True)


break_low = data2015[data2015['Min_temp'] < data['Min_temp']]['Min_temp']
break_high = data2015[data2015['Max_temp'] > data['Max_temp']]['Max_temp']



plt.plot(data.index,data['Min_temp'],'-',color = 'steelblue', label = 'record low')
plt.plot(data.index,data['Max_temp'],'--', color = 'coral', label = 'record high')

plt.fill_between(data.index, data.Max_temp, data.Min_temp,
    color= 'grey',alpha=0.30)

plt.scatter(break_low.index,break_low.values, c='b', label = "2015 break low")
plt.scatter(break_high.index,break_high.values, c='r', label = "2015 break high")

plt.xlabel('month')
plt.ylabel('temperature($^\circ F$ )') 
plt.xticks(np.arange(0,365,31), ['Jan','Feb', 'Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']) 
plt.title('Monthly Temperature Records 2005 - 2014')
plt.legend(loc= "bottom")
