from operator import itemgetter
import pandas as pd

my_dict = {'c1': [1, 2, 3], 'c2': [3, 2, 1], 'c3': [4, 5, 6]}

print(my_dict)

my_dict = pd.DataFrame.from_dict(my_dict)
my_dict.sort_values('c2', axis=0, ascending=True, inplace=True)

for i in range(1):
    print(i)