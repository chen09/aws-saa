import pandas as pd

df = pd.read_csv('./AWS-SAA-C01.zh-CN.csv', header=None)

print(df[0], df[1])
