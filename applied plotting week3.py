import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df


df['mean'] = df.mean(axis = 1)
df['std'] = df.std(axis = 1)
df['95%_confidence'] = stats.norm.ppf(0.975) *(df['std']/math.sqrt(len(df.columns)))



df = df.reset_index()


fig = plt.figure()

ax1 = plt.bar(df['index'], df['mean'],
                 alpha=0.8, 
                label='Mean')


plt.xticks(df['index'], ["1992", "1993", "1994", "1995"])
plt.xlabel('Year')
plt.ylabel('Mean')

plt.errorbar(df['index'], df['mean'], yerr=df['95%_confidence'], color='Black',fmt='none', elinewidth=1.5 ,capthick = 1.5,errorevery=1, alpha=1, ms=4, capsize = 5)

input_value = 41000

ax = fig.add_subplot(111)
ax.axhline(input_value, color= 'orange')

ax.set_facecolor("lightgray")     

plt.text(1991.55, 47000, 'User Input = {:,.0f}'.format(input_value), style='italic', bbox={'facecolor':'k', 'alpha':0.2, 'pad':5})





for i in range(4):
        if (df['mean'][i] - df['95%_confidence'][i]) <= input_value <= (df['mean'][i] + df['95%_confidence'][i]):
            ax1[i].set_color('white')
        elif df['mean'][i] < input_value:
            ax1[i].set_color('blue')
        else:
            ax1[i].set_color('red')
            
