def medal_tally(df):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally=medal_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['Total']=medal_tally['Total'].astype('int')


    return medal_tally



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years,country


def fetch_medal_tally(df,year, country):
    Medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = Medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = Medal_df[Medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = Medal_df[Medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = Medal_df[(Medal_df['Year'] == year) & (Medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold']=x['Gold'].astype('int')
    x['Silver']=x['Silver'].astype('int')
    x['Bronze']=x['Bronze'].astype('int')
    x['Total']=x['Total'].astype('int')
    return x


def data_overtime(df,col):
    data_overtime = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    data_overtime.rename(columns={'index': 'Editions', 'Year': col}, inplace=True)
    return data_overtime


def most_successful_athlete(df,sport):
  temp_df=df.dropna(subset=['Medal'])

  if sport!= 'Overall':
    temp_df=temp_df[temp_df['Sport']==sport]
  x = temp_df["Name"].value_counts().reset_index().head(50).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
  x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
  return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return pt

def most_successful_athlete_incountry(df,country):
  temp_df=df.dropna(subset=['Medal'])

  temp_df=temp_df[temp_df['region']==country]

  x = temp_df["Name"].value_counts().reset_index().head(50).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
  x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
  return x

