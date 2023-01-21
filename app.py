import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocessing,helper

df=pd.read_csv("Data/athlete_events.csv")
region_df=pd.read_csv("Data/noc_regions.csv")
df=df[df['Season']=='Summer']

df=preprocessing.preprocessing(df, region_df)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)
# st.dataframe(df)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Year",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally ")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in "+ str(selected_year)+" Olympics")
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country+" Performance in "+ str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nation = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(Cities)
    with col3:
        st.header('Sports')
        st.title(Sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Athletes')
        st.title(Athletes)
    with col2:
        st.header('Cities')
        st.title(Cities)
    with col3:
        st.header('Nation')
        st.title(Nation)

    nations_overtime=helper.data_overtime(df,'region')
    fig = px.line(nations_overtime, x="Editions", y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    event_overtime = helper.data_overtime(df, 'Event')
    fig = px.line(event_overtime, x="Editions", y='Event')
    st.title("Event over the years")
    st.plotly_chart(fig)

    athlete_overtime = helper.data_overtime(df, 'Name')
    fig = px.line(athlete_overtime, x="Editions", y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    sports_overtime = helper.data_overtime(df, 'Sport')
    fig = px.line(sports_overtime, x="Editions", y='Sport')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    select_sport=st.selectbox("Select a Sport",sport_list)
    athlete_list=helper.most_successful_athlete(df,select_sport)
    st.table(athlete_list.reset_index(drop=True))


if user_menu=='Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    select_country=st.sidebar.selectbox("Select a Country",country_list)

    country_df=helper.yearwise_medal_tally(df,select_country)
    fig = px.line(country_df, x="Year", y='Medal')
    st.title(select_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(select_country+" excels in the following Sports")
    pt=helper.country_event_heatmap(df,select_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)


    st.title("Top athletes of "+ select_country)
    top_df=helper.most_successful_athlete_incountry(df,select_country)
    st.table(top_df)


if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])


    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    X=[]
    name=[]
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
       'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
       'Alpinism', 'Aeronautics']
    for sport in famous_sports:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        X.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(X, name,show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    # st.title("Sport-Wise Distribution of Age (Gold Medal)")
    # st.plotly_chart(fig)
