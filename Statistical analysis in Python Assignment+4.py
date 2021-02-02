
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[5]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[12]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df = pd.read_table(r'university_towns.txt', sep='\n', header=None, names=['RegionName'])
    df.insert(0, 'State', df['RegionName'].str.extract('(.*)\[edit\]', expand=False).ffill())
    df['RegionName'] = df['RegionName'].str.replace(r' \(.+$', '')
    df = df[~df['RegionName'].str.contains('\[edit\]')].reset_index(drop=True)
    return df

get_list_of_university_towns()


# In[7]:


def get_recession_start():
    GDP = pd.read_excel('gdplev.xls',usecols =[4,6])
    GDP = GDP[219:]
    GDP.columns = ['Quarter','GDP chained 2009 dollars']
    GDP.set_index('Quarter', inplace = True)
    lst_start = []
    lst_end =[]
    recession = False
    for i in range(1, len(GDP)-1):
        if not recession and (GDP.iloc[i-1, 0] > GDP.iloc[i, 0] > GDP.iloc[i+1, 0]):
            recession = True
            lst_start.append(GDP.index[i])
        elif recession and (GDP.iloc[i-1, 0] < GDP.iloc[i, 0] < GDP.iloc[i+1, 0]):
            recession = False
            lst_end.append(GDP.index[i])
            return lst_start[0]
get_recession_start()


# In[8]:


def get_recession_end():
    GDP = pd.read_excel('gdplev.xls',usecols =[4,6])
    GDP = GDP[219:]
    GDP.columns = ['Quarter','GDP chained 2009 dollars']
    GDP.set_index('Quarter', inplace = True)
    lst_start = []
    lst_end =[]
    recession = False
    for i in range(1, len(GDP)-1):
        if not recession and (GDP.iloc[i-1, 0] > GDP.iloc[i, 0] > GDP.iloc[i+1, 0]):
            recession = True
            lst_start.append(GDP.index[i])
        elif recession and (GDP.iloc[i-1, 0] < GDP.iloc[i, 0] < GDP.iloc[i+1, 0]):
            recession = False
            lst_end.append(GDP.index[i])
            return lst_end[0]
get_recession_end()


# In[9]:


def get_recession_bottom():
    GDP = pd.read_excel('gdplev.xls',usecols =[4,6])
    GDP = GDP[219:]
    GDP.columns = ['Quarter','GDP chained 2009 dollars']
    GDP.set_index('Quarter', inplace = True)
    lst_start = []
    lst_end =[]
    recession = False
    for i in range(1, len(GDP)-1):
        if not recession and (GDP.iloc[i-1, 0] > GDP.iloc[i, 0] > GDP.iloc[i+1, 0]):
            recession = True
            lst_start.append(GDP.index[i])
        elif recession and (GDP.iloc[i-1, 0] < GDP.iloc[i, 0] < GDP.iloc[i+1, 0]):
            recession = False
            lst_end.append(GDP.index[i])
    recession = GDP[lst_start[0]:lst_end[0]]
    recession.reset_index(inplace = True)
    bottom = recession.loc[recession['GDP chained 2009 dollars'] == recession['GDP chained 2009 dollars'].min(),'Quarter'].iloc[0]
    return bottom

get_recession_bottom()


# In[14]:


def convert_housing_data_to_quarters():
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing['State'].replace(states,inplace = True)
    housing = housing.set_index(["State","RegionName"])
    housing = housing.iloc[:,49:250]
    def quarters(col):
        if col.endswith(("01","02","03")):
            s = col[:4] + "q1"
        elif col.endswith(("04","05","06")):
            s = col[:4] + "q2"
        elif col.endswith(("07","08","09")):
            s = col[:4] + "q3"
        else:
            s = col[:4] + "q4"
        return s
    housing = housing.groupby(quarters, axis = 1).mean()
    return housing

convert_housing_data_to_quarters()


# In[16]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
     
    towns = get_list_of_university_towns()
    startdate = get_recession_start()
    bottomdate = get_recession_bottom()
    housing = convert_housing_data_to_quarters()
    
    housing = housing.reset_index()
    housing['recession_diff'] = housing[startdate] - housing[bottomdate]
    
    towns_houses = pd.merge(housing, towns, how='inner', on=['State', 'RegionName'])
    towns_houses['ctown'] = True
    houses = pd.merge(housing, towns_houses, how='outer', on = ['State', 'RegionName',
                                                              bottomdate, startdate, 
                                                              'recession_diff'])
    houses['ctown'] = houses['ctown'].fillna(False)
    unitowns = houses[houses['ctown'] == True]
    not_unitowns = houses[houses['ctown'] == False]
    
    t, p = ttest_ind(unitowns['recession_diff'].dropna(), not_unitowns['recession_diff'].dropna())
    different = True if p < 0.01 else False
    betters = "university town" if unitowns['recession_diff'].mean() < not_unitowns['recession_diff'].mean() else "non-university town"
    
    return different,p,betters

run_ttest()


# In[ ]:




