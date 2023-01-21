import pandas as pd


def preprocessing(df,region_df):
    #merging df with region_df
    df=df.merge(region_df,on='NOC',how='left')
    #dropping duplicates
    df.drop_duplicates(inplace=True)
    #one-hot encodinng medals
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df