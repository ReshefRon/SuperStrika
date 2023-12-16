import pandas as pd
df = pd.read_csv("DATA/SuperStrika.csv")
df = df[['Name','Team Code','Name for URL']]
df = df.drop_duplicates().reset_index()
df.to_csv('TeamCodes.csv', index=False)