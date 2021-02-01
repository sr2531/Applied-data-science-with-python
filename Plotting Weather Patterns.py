
# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.



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
