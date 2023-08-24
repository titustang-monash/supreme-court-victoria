'''
This script merges multiple copies of the same data in different files and then removes duplicates.
The aim is to get a non-repeating union of the files.
'''


import os
import pandas as pd

load_path = 'D:/Desktop/SCV/Duplicates'
save_path = 'D:/Desktop/SCV/'

all_data = []
for year in range(2018, 2023+1):
    dfa = pd.read_csv(os.path.join(load_path, str(year)+'a.csv'))
    dfb = pd.read_csv(os.path.join(load_path, str(year) + 'b.csv'))
    df = pd.concat([dfa, dfb])
    df = df.drop_duplicates()

    print(year)
    print(str(year)+'a', len(dfa.index), 'rows')
    print(str(year) + 'a', len(dfa.index)- len(dfa.drop_duplicates().index), 'duplicate rows')

    print(str(year)+'b', len(dfb.index), 'rows')
    print(str(year) + 'b', len(dfb.index) - len(dfb.drop_duplicates().index), 'duplicate rows')

    print(str(year), 'Merged', len(df.index), 'rows')

    all_data.append(df)

all_data = pd.concat(all_data)
print('Final file', len(all_data.index), 'rows')
all_data.to_csv(os.path.join(save_path, 'SCV_data.csv'), index=False)
