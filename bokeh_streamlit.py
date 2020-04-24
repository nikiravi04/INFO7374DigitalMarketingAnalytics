import markdown
import pandas as pd
import streamlit as st
import io
from typing import List, Optional
from itertools import chain
from collections import Counter
import random
import pickle
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from bokeh.palettes import Spectral

from PIL import Image
import requests
from io import BytesIO

import recommender
from recommender import make_prediction


def main():
    @st.cache
    def load_data():
        df_final = pd.read_csv('Data/final_with_genre.csv')
        return df_final

    df_final = load_data()


    st.sidebar.title("Video Games Analytics")
    genre = st.sidebar.radio(
      '''
      Choose an option
      ''',
     ('Home','Recommender System','Streamer Analytics', 'Viewer Analytics', 'Churn Analytics'))

    if genre == 'Home':
        st.markdown(
        """
        # What is a video game streaming application? 

        Who does not like video games? From the very famous mario series to Fortnite, video gaming has come a long way. 
        Don't you remember fighting for a joystick with your siblings or friends when video games allowed only two players at a time ? 
        Now with the boom in technology, the gaming industry has leveled up its standards by allowing 100’s to 1000 players at a time 
        to not just play but also to interact and live stream their play time. 

        For those unfamiliar with it, Twitch is a streaming video website where content creators attract wide audiences of viewers and 
        subscribers by streaming themselves while they play popular video games or other entertaining content. 
        In 2018 alone, over 1 million years of content was consumed on Twitch, with over 4 million unique monthly streamers providing it. 
        As you can imagine, with so many choices of what to watch or what to play, 
        the streamers are competing with each other for viewers and dedicated subscribers.

        ## What is the Purpose of this App?
        The three base principles of making money for Video-game streaming applications are Partner Programs, Customer behaviour and Subscriptions. 
        Our Application consolidates all these three principles.

        ## 1) Recommendation
        Streamers stand a chance to partner with Video game streaming applications.The base requirements to partner with the streaming service is quality content, 
        average concurrent viewership and a stream frequency of at least three days per week.In order to increase their viewership count, our App helps to recommend 
        streamers on what games to stream so that the they can target the right audience. 
        
        ## 2) RFE
        RFE stands for Recency, Frequency, and Engagement value each corresponding to some key customer trait. These metrics are important indicators of a customer’s behaviour because 
        frequency and monetary value affects a customer’s lifetime value, and recency affects retention.

        ## 3) Churn Analytics 
        This shows us the total number of customers lost over a period of time and their respective churn dates.It is important to know the
        churn details of the users as it helps in understanding financial aspect of the company.

        ## Who can use it?
        This App will provide all details required for the marketing team in just a click.It will help them understand the customer activities, behaviour and 
        market conditions. Analyzing these trends will in turn help the company decide which products and services to sell, to which customers and at what price & time.
        Thereby improving the company's business and revenue."""
        )
        st.image('Images/video_game.jpg')

    elif genre == 'Recommender System':
        st.title('Recommender System')

        st.markdown('''

            ### Predicting Similar Genres/Games Based on Streamer experience (user-based similarity)

            Given the name of a streamer, list of genres they enter, and a list of games they say
            they play, generate predictions based on similar genres and similar games to both
            what they enter into our website and what our database has recorded for them.

            ### Why marketing analysts need a backend recommendation system?

            Of course, to help streamers/gamers to find the correct games to stream 
            and to enjoy an individualized experience. On top of that, it is a
            great tool to retain the existing viewer base to make marketing more efficient.

            ''')

        def load_models(user_name):
            with open( "Data/genres.pkl", "rb" ) as f:
                user_genres = pickle.load(f)
            user_genre = user_genres[user_genres['user_name']==user_name]

            with open( "Data/games.pkl", "rb" ) as f:
                user_games = pickle.load(f)
            user_game = user_games[user_games['user_name']==user_name]

            return (user_genres, user_games)

        

        streamer_name = st.text_input('What is your streamer name? ', 'Anomaly')
        #streamer_genres = st.text_input('Which game genres do you currently stream? ', 'Action')
        #streamer_games = st.text_input('Which games do you currently stream? ', 'Fortnite')

        
        if st.button('Lets Recommend!'):
            
            
            if streamer_name in list(df_final['user_name'].unique()):

                user_genres, user_games = load_models(streamer_name)
                user_genres_lst = list(user_genres['game_genres'])
                user_games_lst = list(user_games['game_name'])

                streamer_genres = random.choices(user_genres_lst, k=4)
                streamer_games = random.choices(user_games_lst, k=9)
                recommendations, pic_urls = make_prediction(streamer_name,streamer_genres,streamer_games)

                st.write('Recommended Games for :',streamer_name)
                recommendations['game_recommendations'] = list(recommendations['game_recommendations'])
                pic_urls = list(pic_urls)

                img_list = []
                for game_name,game_pic in zip(recommendations['game_recommendations'],pic_urls):
                    response = requests.get(game_pic)
                    img = Image.open(BytesIO(response.content))
                    img_list.append(img)
                game_names = recommendations['game_recommendations']
                st.image([img_list[0],img_list[1],img_list[2],img_list[3],img_list[4]],width=100, caption = game_names[:5])
                st.image([img_list[5],img_list[6],img_list[7],img_list[8],img_list[9]],width=100, caption = game_names[5:])
               
                st.write('Recommended Genres for :', streamer_name)
                recommendations['genre_recommendations'] = list(recommendations['genre_recommendations'])
                # st.write(recommendations['genre_recommendations'])
                #recommemded genre viz
                recommendation = pd.DataFrame(recommendations['genre_recommendations'],columns=['recommended_genre'])
                recommendation['recommended_genre'].unique()
                game_genre_initial = recommendation['recommended_genre'].map(lambda x: x.split(',')).values.tolist()
                all_game_genre = list(chain(*game_genre_initial))
                #count the genres 
                count_recommended_genre = Counter(all_game_genre)
                count_recommended_genre_df = pd.DataFrame.from_dict(count_recommended_genre, orient='index').reset_index()
                count_recommended_genre_df = count_recommended_genre_df.rename(columns={'index':'genres_recommended', 0:'count'})

                fig_genre = px.pie(count_recommended_genre_df,values='count',names='genres_recommended')
                fig_genre.update_traces(hoverinfo='label+percent',textfont_size=12)
                st.plotly_chart(fig_genre)

            else:
                st.write('Username not valid! Check User Name.')
        else:
            st.write('Shoot! Type in your streamer info')



    elif genre == 'Streamer Analytics':
        st.title('Streamer Analytics')


        if st.checkbox('Show Data'):
            df_final #dataframe

        st.markdown("""
            ## Top 10 Streamers
            """)
        df_user_game_name = pd.DataFrame(df_final.groupby('user_name')['viewer_count'].sum())
        df_top_10_user_name = df_user_game_name.nlargest(10,'viewer_count')

        top_10_users= pd.DataFrame(df_top_10_user_name.groupby('user_name')['viewer_count'].sum()).reset_index()
        top_10_users_color = list(Spectral[len(top_10_users)])
        fig_top_10_users = go.Figure(data=go.Bar(x=top_10_users['viewer_count'],
                                        y=top_10_users['user_name'],
                                        text=top_10_users['user_name'],orientation ='h',marker_color=top_10_users_color)) 
         
        fig_top_10_users.update_layout(height=600,width=600,yaxis={'categoryorder':'category descending'},
                         plot_bgcolor='rgba(0,0,0,0)',xaxis_title='Viewer Count', yaxis_title='Streamers')
 
        st.plotly_chart(fig_top_10_users, use_container_width=True)

        st.markdown("""
            ## Top 10 Games Streamed By Streamers
            """)
        df_group_game_name = pd.DataFrame(df_final.groupby('game_name')['viewer_count'].sum())
        df_top_10_game_name = df_group_game_name.nlargest(10,'viewer_count')

        top_10_games= pd.DataFrame(df_top_10_game_name.groupby('game_name')['viewer_count'].sum()).reset_index()
        top_10_games_color = list(Spectral[len(top_10_users)])
        fig_top_10_games = go.Figure(data=go.Bar(x=top_10_games['viewer_count'],
                                        y=top_10_games['game_name'],
                                        text=top_10_games['game_name'],orientation ='h',marker_color=top_10_games_color)) 
         
        fig_top_10_games.update_layout(height=600,width=600,yaxis={'categoryorder':'category ascending'},
                         plot_bgcolor='rgba(0,0,0,0)',xaxis_title='Viewer Count', yaxis_title='Streamers Game Name')
        
        st.plotly_chart(fig_top_10_games, use_container_width=True)


        st.markdown("""
            ## Top 10 Genres Streamed By Streamers
            """)
        df_group_game_genres = pd.DataFrame(df_final.groupby('game_genres')['viewer_count'].sum())
        df_top_10_game_genres = df_group_game_genres.nlargest(10,'viewer_count')

        top_10_genres= pd.DataFrame(df_top_10_game_genres.groupby('game_genres')['viewer_count'].sum()).reset_index()
        top_10_genres_color = list(Spectral[len(top_10_users)])
        fig_top_10_genres = go.Figure(data=go.Bar(x=top_10_genres['viewer_count'],
                                        y=top_10_genres['game_genres'],
                                        text=top_10_genres['game_genres'],orientation ='h',marker_color=top_10_genres_color)) 
         
        fig_top_10_genres.update_layout(height=600,width=600,yaxis={'categoryorder':'category descending'},
                         plot_bgcolor='rgba(0,0,0,0)',xaxis_title='Viewer Count', yaxis_title='Streamers Game Genre')
        
        st.plotly_chart(fig_top_10_genres, use_container_width=True)



    elif genre == 'Viewer Analytics':

        st.title('Viewer Analytics')

        st.markdown("## ** ♟ Customer Segmentation using RFE ** ♟ ")

        @st.cache
        def load_data():
            tx_user = pd.read_csv("Data/user_rfe_viz.csv")
            return tx_user
        def load_data():
            tx_ltv_rfe = pd.read_csv("Data/tf_ltv_viz.csv")
            return tx_ltv_rfe    

        tx_user=load_data()
        tx_ltv_rfe = load_data()

        if st.checkbox('Show Data'):
                     st.write(tx_user)
                     st.write(tx_ltv_rfe)
    

        st.markdown(""" RFE analysis is a simple way of segmenting existing customers based on engagement with the application.

        ->Recency: date of the most recent visitors

        ->Frequency: number of times visited

        ->Engagement: total duration of the visit""")

        st.markdown("*Our top 10 customers based of RFE Analysis*")

        top_10 = tx_user[tx_user['OverallScore']==6].sort_values('Engagement', ascending=False).head(10)

        top_11 = top_10[["viewer_id", "Segment"]]

        st.write(top_11)

        #Engagement vs Frequency
        tx_graph = tx_user
        plot_data = [
            go.Scatter(
                x=tx_graph.query("Segment == 'Low-Value'")['Frequency'],
                y=tx_graph.query("Segment == 'Low-Value'")['Engagement'],
                mode='markers',
                name='Low',
                marker= dict(size= 7,
                    line= dict(width=1),
                    color= 'purple',
                    opacity= 0.8
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'Mid-Value'")['Frequency'],
                y=tx_graph.query("Segment == 'Mid-Value'")['Engagement'],
                mode='markers',
                name='Mid',
                marker= dict(size= 9,
                    line= dict(width=1),
                    color= 'green',
                    opacity= 0.5
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'High-Value'")['Frequency'],
                y=tx_graph.query("Segment == 'High-Value'")['Engagement'],
                mode='markers',
                name='High',
                marker= dict(size= 11,
                    line= dict(width=1),
                    color= 'yellow',
                    opacity= 0.9
                   )
            ),
        ]

        plot_layout = go.Layout(
                yaxis= {'title': "Engagement"},
                xaxis= {'title': "Frequency"},
                title='Engagement Vs Frequency'
            )
        fig5 = go.Figure(data=plot_data, layout=plot_layout)
        #pyoff.iplot(fig)
        st.plotly_chart(fig5, use_container_width=True)

        #Engagement  Recency

        plot_data = [
            go.Scatter(
                x=tx_graph.query("Segment == 'Low-Value'")['Recency'],
                y=tx_graph.query("Segment == 'Low-Value'")['Engagement'],
                mode='markers',
                name='Low',
                marker= dict(size= 7,
                    line= dict(width=1),
                    color= 'purple',
                    opacity= 0.8
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'Mid-Value'")['Recency'],
                y=tx_graph.query("Segment == 'Mid-Value'")['Engagement'],
                mode='markers',
                name='Mid',
                marker= dict(size= 9,
                    line= dict(width=1),
                    color= 'green',
                    opacity= 0.5
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'High-Value'")['Recency'],
                y=tx_graph.query("Segment == 'High-Value'")['Engagement'],
                mode='markers',
                name='High',
                marker= dict(size= 11,
                    line= dict(width=1),
                    color= 'yellow',
                    opacity= 0.9
                   )
            ),
        ]

        plot_layout = go.Layout(
                yaxis= {'title': "Engagement"},
                xaxis= {'title': "Recency"},
                title='Engagement Vs Recency'
            )
        fig6 = go.Figure(data=plot_data, layout=plot_layout)
        #pyoff.iplot(fig)
        st.plotly_chart(fig6, use_container_width=True)


        # Engagement  vs Frequency
        tx_graph = tx_user.query("Engagement < 50000 and Frequency < 2000")

        plot_data = [
            go.Scatter(
                x=tx_graph.query("Segment == 'Low-Value'")['Recency'],
                y=tx_graph.query("Segment == 'Low-Value'")['Frequency'],
                mode='markers',
                name='Low',
                marker= dict(size= 7,
                    line= dict(width=1),
                    color= 'purple',
                    opacity= 0.8
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'Mid-Value'")['Recency'],
                y=tx_graph.query("Segment == 'Mid-Value'")['Frequency'],
                mode='markers',
                name='Mid',
                marker= dict(size= 9,
                    line= dict(width=1),
                    color= 'green',
                    opacity= 0.5
                   )
            ),
                go.Scatter(
                x=tx_graph.query("Segment == 'High-Value'")['Recency'],
                y=tx_graph.query("Segment == 'High-Value'")['Frequency'],
                mode='markers',
                name='High',
                marker= dict(size= 11,
                    line= dict(width=1),
                    color= 'yellow',
                    opacity= 0.9
                   )
            ),
        ]

        plot_layout = go.Layout(
                yaxis= {'title': "Frequency"},
                xaxis= {'title': "Recency"},
                title='Frequency Vs Recency'
            )
        fig7 = go.Figure(data=plot_data, layout=plot_layout)
        #pyoff.iplot(fig)
        st.plotly_chart(fig7, use_container_width=True)


        #ltv rfe relation

        plot_data = [
            go.Scatter(
                x=tx_ltv_rfe.query("Segment == 'Low-Value'")['OverallScore'],
                y=tx_ltv_rfe.query("Segment == 'Low-Value'")['m6_Engagement'],
                mode='markers',
                name='Low',
                marker= dict(size= 7,
                    line= dict(width=1),
                    color= 'blue',
                    opacity= 0.8
                   )
            ),
                go.Scatter(
                x=tx_ltv_rfe.query("Segment == 'Mid-Value'")['OverallScore'],
                y=tx_ltv_rfe.query("Segment == 'Mid-Value'")['m6_Engagement'],
                mode='markers',
                name='Mid',
                marker= dict(size= 9,
                    line= dict(width=1),
                    color= 'green',
                    opacity= 0.5
                   )
            ),
                go.Scatter(
                x=tx_ltv_rfe.query("Segment == 'High-Value'")['OverallScore'],
                y=tx_ltv_rfe.query("Segment == 'High-Value'")['m6_Engagement'],
                mode='markers',
                name='High',
                marker= dict(size= 11,
                    line= dict(width=1),
                    color= 'red',
                    opacity= 0.9
                   )
            ),
        ]

        plot_layout = go.Layout(
                yaxis= {'title': "LTV"},
                xaxis= {'title': "RFE Score"},
                title='LTV vs RFE'
            )
        fig8 = go.Figure(data=plot_data, layout=plot_layout)
        #pyoff.iplot(fig)
        st.plotly_chart(fig8, use_container_width=True)

        st.markdown("Positive correlation is quite visible. High RFM score means high LTV")


    elif genre == 'Churn Analytics':
        st.title("Churn Analytics")

        st.markdown("""This churn model is a mathematical representation 
            of how churn impacts our business. 
        Churn calculations are built on existing data i.e the number of 
        subsrcibers who left our service during a given time period (2018-2020)
        According to the business needs, the number of days and 
        when to make predictions can be adjusted

        We have two scenarios:

        (i) Monthly Churn 
        (ii) Bimonthly Churn """)

        # st.image('Images/churn.png')


        @st.cache
        def load_data():
            Transaction = pd.read_csv('Data/trans.csv',parse_dates=['transaction_date', 'membership_expire_date'], infer_datetime_format = True)
            return Transaction

        Transaction=load_data()

        @st.cache
        def load_data():
            cutoff_times = pd.read_csv('Data/laMon.csv',parse_dates = ['cutoff_time'])
            cutoff_times = cutoff_times.drop_duplicates(subset = ['user_id', 'cutoff_time'])
            return cutoff_times

        cutoff_times = load_data()

        @st.cache
        def load_data():
            Churned = pd.read_csv('Data/ChurnMon.csv',parse_dates = ['cutoff_time', 'churn_date'])
            return Churned

        Churned= load_data()

        @st.cache
        def load_data():
            cutoff_times_1 = pd.read_csv('Data/laBi.csv',parse_dates = ['cutoff_time'])
            cutoff_times_1 = cutoff_times_1.drop_duplicates(subset = ['user_id', 'cutoff_time'])
            return cutoff_times_1

        cutoff_times_1 = load_data()

        @st.cache
        def load_data():
            ChurnedBiM = pd.read_csv('Data/ChurnBi.csv',parse_dates = ['cutoff_time','churn_date'])
            return ChurnedBiM
            
        ChurnedBiM= load_data()

        if st.checkbox('Show Data'):
                     st.write(Transaction)
                     #st.write(cutoff_times)
                     st.write(Churned)
                     #st.write(cutoff_times_1)
                     st.write(ChurnedBiM)

                    
                
        st.title('Monthly Churn')

        st.markdown("""Monthly churn is the one where prediction labels are made on a monthly basis, if any user goes without a membership for 
        more than 31 days, they are a churned customer""")

        df= cutoff_times['label'].value_counts()
        a_dictionary = dict(df)
        keys = list(a_dictionary.keys())
        values = list(a_dictionary.values())
        colors = ['lightslategray',]*2
        colors[1] = 'crimson'
        fig = go.Figure([go.Bar(x=keys, y=values,marker_color=colors,
                                text=values,
                    textposition='auto')])
        fig.update_layout(title_text='Monthly Churn',xaxis_title="Churn Prediction",
            yaxis_title="Count",)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""here 0 represents the subscribers who have not churned and 1 represents subscribers who have churned""")

        st.markdown("""### Number of Subscribes lost in the past through Monthly Churn ###""")

        totalchurn=Churned.groupby(Churned['churn_date'].dt.year)['user_id'].count().sort_values()
        total=totalchurn.to_frame(name='Numbers lost').reset_index()
        total1=total.rename(columns={"churn_date": "Year", "Numbers lost": "Numbers lost"})
        st.write(total1)

        st.title('Bimonthly Churn')

        st.markdown("""Bimonthly churn is the one where prediction labels are made on a bimonthly basis, if any user goes without a membership for 
        more than 15 days, they are a churned customer""")


        df_1= cutoff_times_1['label'].value_counts()
        a_dictionary_1 = dict(df_1)
        keys_1 = list(a_dictionary_1.keys())
        values_1 = list(a_dictionary_1.values())
        colors = ['lightslategray',]*2
        colors[1] = 'crimson'
        fig1 = go.Figure([go.Bar(x=keys_1, y=values_1,marker_color=colors,
                                text=values_1,
                    textposition='auto')])
        fig1.update_layout(title_text='Bimonthly Churn',xaxis_title="Churn Prediction",
            yaxis_title="Count",)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("""here 0 represents the subscribers who have not churned and 1 represents subscribers who have churned""")
        st.markdown("""### Number of Subscribes lost in the past through Bimonthly Churn ###""")

        totalchurn1=ChurnedBiM.groupby(ChurnedBiM['churn_date'].dt.year)['user_id'].count().sort_values()
        total11=totalchurn1.to_frame(name='Numbers lost').reset_index()
        total111=total11.rename(columns={"churn_date": "Year", "Numbers lost": "Numbers lost"})
        st.write(total111)

        st.title("Churn Statistics")
        st.markdown(""" This year-wise stats shows the Monthly vs Bimonthly churn for all 12 months in a year """)

        include = Churned[Churned['churn_date'].dt.year == 2018]
        include1 = Churned[Churned['churn_date'].dt.year == 2019]
        include2 = Churned[Churned['churn_date'].dt.year == 2020]

        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        x = pd.DataFrame(include.groupby(include['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        x['churn_date'] = pd.Categorical(x['churn_date'], categories=months, ordered=True)
        x1=x.sort_values('churn_date')

        y = pd.DataFrame(include1.groupby(include1['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        y['churn_date'] = pd.Categorical(y['churn_date'], categories=months, ordered=True)
        y1=y.sort_values('churn_date')

        z = pd.DataFrame(include2.groupby(include2['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        z['churn_date'] = pd.Categorical(z['churn_date'], categories=months, ordered=True)
        z1=z.sort_values('churn_date')


        exclude = ChurnedBiM[ChurnedBiM['churn_date'].dt.year == 2018]
        exclude1 = ChurnedBiM[ChurnedBiM['churn_date'].dt.year == 2019]
        exclude2 = ChurnedBiM[ChurnedBiM['churn_date'].dt.year == 2020] 

        u = pd.DataFrame(exclude.groupby(exclude['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        u['churn_date'] = pd.Categorical(u['churn_date'], categories=months, ordered=True)
        u1=u.sort_values('churn_date')

        v = pd.DataFrame(exclude1.groupby(exclude1['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        v['churn_date'] = pd.Categorical(v['churn_date'], categories=months, ordered=True)
        v1=v.sort_values('churn_date')

        w = pd.DataFrame(exclude2.groupby(exclude2['churn_date'].dt.strftime('%B'))['user_id'].count()).reset_index()
        w['churn_date'] = pd.Categorical(w['churn_date'], categories=months, ordered=True)
        w1=w.sort_values('churn_date')

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=u1['churn_date'], y=u1['user_id'],
                            mode='lines+markers',
                            name='Bimonthly'))
        fig2.add_trace(go.Scatter(x=x1['churn_date'], y=x1['user_id'],
                            mode='lines+markers',
                            name='Monthly'))
        fig2.update_layout(title_text='Churn for the year 2018',xaxis_title="Months",
            yaxis_title="Total Count")
        st.plotly_chart(fig2, use_container_width=True) 

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=v1['churn_date'], y=v1['user_id'],
                            mode='lines+markers',
                            name='bimonthly'))
        fig3.add_trace(go.Scatter(x=y1['churn_date'], y=y1['user_id'],
                            mode='lines+markers',
                            name='monthly'))
        fig3.update_layout(title_text='Churn for the year 2019',xaxis_title="Months",
            yaxis_title="Total Count")
        st.plotly_chart(fig3, use_container_width=True) 

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=w1['churn_date'], y=w1['user_id'],
                            mode='lines+markers',
                            name='bimonthly'))
        fig4.add_trace(go.Scatter(x=z1['churn_date'], y=z1['user_id'],
                            mode='lines+markers',
                            name='monthly'))
        fig4.update_layout(title_text='Churn for the year 2020',xaxis_title="Months",
            yaxis_title="Total Count")
        st.plotly_chart(fig4, use_container_width=True) 


        st.title("""Subscriber Churn & Transaction Details""")
        st.markdown("""Information like Subscribers churn date, # days to churn, renewal details, payment plan details, transaction date, membership expiry date and membership cancellation details can be viewed""")
        st.markdown("Monthly Churn Information")
        User_id = st.multiselect('Select a User ID to find out Monthly Churn', Churned['user_id'].unique())
        ns= Transaction[(Transaction['user_id'].isin(User_id))] 
        new_df = Churned[(Churned['user_id'].isin(User_id))] 

        #write dataframe to screen
        st.write(new_df)
        st.write(ns)
            
        st.markdown("Bimonthly Churn Information")
        User_id_1 = st.multiselect('Select a User ID to find out BiMonthly Churn', ChurnedBiM['user_id'].unique())
        ns_1= Transaction[(Transaction['user_id'].isin(User_id_1))]  
        new_df_1 = ChurnedBiM[(ChurnedBiM['user_id'].isin(User_id_1))] 

        #write dataframe to screen
        st.write(new_df_1)
        st.write(ns_1)

        st.markdown("Here the Payment method ID is encrypted due to Subscriber Privacy ")


   

main()