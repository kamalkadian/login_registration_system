import streamlit as st
import pandas as pd
import preprocessor, medaltally
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")
df=preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    "Select an Option",
    ("Medal Tally","Overall Analysis", "Country-wise Analysis","Athlete wise Analysis")
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years,country=medaltally.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select country",country)

    medal_tally = medaltally.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year=="Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year)  + " Olympics")
    if selected_year=="Overall" and selected_country != "Overall":
        st.title(selected_country + " overall performance")
    if selected_year!= "Overall" and selected_country!="Overall":
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)
if user_menu=="Overall Analysis":
    editions=df["Year"].unique().shape[0]-1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    nations=df["region"].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    nations_over_time=medaltally.participating_nations_over_time(df)
    st.title("Nations in different years")
    fig = px.line(nations_over_time, x="Edition", y="countries")
    st.plotly_chart(fig)

    st.title("Most successful Athletes")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")

    selected_sport=st.selectbox("Select a Sport",sport_list)
    x=medaltally.mostsuccessful(df,selected_sport)
    st.table(x)

if user_menu == "Country-wise Analysis":

    st.sidebar.title("Country-wise Analysis")

    country_list=df["region"].dropna().unique().tolist()
    country_list.sort()


    selected_country=st.sidebar.selectbox("Select a Country",country_list)

    country_df=medaltally.yearwise_medal_tally(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country + "Medal Tally over the years")
    st.plotly_chart(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df =  medaltally.mostsuccessful_countrywise(df, selected_country)
    st.table(top10_df)
if user_menu=="Athlete wise Analysis":
    athlete_df=df.drop_duplicates(subset=["Name","region"])

    x1=athlete_df["Age"].dropna()
    x2=athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    st.title("Distribution of Age")

    fig=ff.create_distplot([x1,x2,x3,x4],["overall Age","Gold Medalist", "Silver Medalist","Bronze Medalist"],
                           show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)

    st.plotly_chart(fig)

    st.title("Men vs women participation over the years")
    final=medaltally.men_vs_women(df)
    fig=px.line(final,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)

