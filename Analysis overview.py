import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


df = pd.read_csv(os.path.join('D:/Desktop/SCV/', 'SCV_data.csv'))
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
print('Dataframe has', len(df.index), 'rows')
# pd.set_option('display.min_rows', 100)
# for i in ['Court', 'Case number', 'Location', 'Matter', 'Hearing']:
#     print(i)
#     print(df[i].value_counts())
#     print('ISNA', np.sum(df[i].isna()))
#     print('----------------------------\n\n')


# df['y_m'] = df['Date'].dt.to_period('M') #
df['y_m'] = df['Date'].dt.year * 100 + df['Date'].dt.month


virtual = df[df['Hearing'].str.contains('Virtual Hearing', case=False)]
real = df[~df['Hearing'].str.contains('Virtual Hearing', case=False)]


xlabels = []
virtualcounts = []
realcounts = []
totalcounts = []
m = 9
for y in range(2018, 2023+1):

    for j in range(12):
        pint = y * 100 + m
        pstr = '{}_{:02d}'.format(y, m)
        xlabels.append(pstr)

        vc = len(virtual[virtual['y_m']==pint].index)
        virtualcounts.append(vc)
        rc = len(real[real['y_m'] == pint].index)
        realcounts.append(rc)
        totalcounts.append(vc+rc)


        m += 1
        if m >12:
            m = 1
            break


plt.figure(figsize=(12,8))
plt.plot(xlabels, virtualcounts, 'b', label='Virtual')
plt.plot(xlabels, realcounts, 'r', label='Real')
plt.plot(xlabels, totalcounts, 'k', label='Total')

plt.legend(loc='upper right')
plt.xticks(rotation=90)
plt.show()

















