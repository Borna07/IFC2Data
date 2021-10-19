# def funkcija():
#     global a    
#     a = "DREK"
#     return a
# funkcija()

# print(a)

import pandas as pd

# initialize list of lists
data = [['tom', 10], ['nick', 15], ['juli', 14]]
 
# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['Name', 'Age'])
 
# print dataframe.
df = df.to_excel()

print(df)