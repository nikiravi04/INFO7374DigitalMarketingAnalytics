import markdown
import pandas as pd
import streamlit as st
import io
from typing import List, Optional

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


    st.sidebar.title("Video Games Analytics")
    genre = st.sidebar.radio(
      '''
      Choose an option
      ''',
     ('Home','Streamer Analytics', 'Viewer Analytics', 'Recommender System'))

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
        """
        )

    if genre == 'Streamer Analytics':
        st.title('Streamer Analytics')

        @st.cache
        def load_data():
           df_final = pd.read_csv('Data/final_with_genre.csv')
           return df_final

        df_final = load_data()

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
        st.title("Viewer Analytics")

    elif genre == 'Recommender System':
        st.title('Recommender System')

        streamer_name = st.text_input('What is your streamer name? ', 'Ninja')
        streamer_genres = st.text_input('Which game genres do you currently stream? ', 'Action')
        streamer_games = st.text_input('Which games do you currently stream? ', 'Fortnite')

        
        if st.button('Lets Recommend!'):
            # st.write('Streamer name', streamer_name)
            # st.write('Streamer game genre', streamer_genres)
            # st.write('Streamer game name', streamer_games)
            recommendations, pic_urls = make_prediction(streamer_name,streamer_genres,streamer_games)

            st.write('Recommended Genres for :', streamer_name)
            recommendations['genre_recommendations'] = list(recommendations['genre_recommendations'])
            st.write(recommendations['genre_recommendations'])

            st.write('Recommended Games for :',streamer_name) 
            recommendations['game_recommendations'] = list(recommendations['game_recommendations'])
            pic_urls = list(pic_urls)

            for game_name,game_pic in zip(recommendations['game_recommendations'],pic_urls):
                response = requests.get(game_pic)
                img = Image.open(BytesIO(response.content))
                st.image(img,width=100,caption = game_name)
   
        else:
            st.write('Shoot! Type in your streamer info')


        # class Cell:
        #     """A Cell can hold text, markdown, plots etc."""
        #     def __init__(
        #         self,
        #         class_: str = None,
        #         grid_column_start: Optional[int] = None,
        #         grid_column_end: Optional[int] = None,
        #         grid_row_start: Optional[int] = None,
        #         grid_row_end: Optional[int] = None,
        #         ):
        #         self.class_ = class_
        #         self.grid_column_start = grid_column_start
        #         self.grid_column_end = grid_column_end
        #         self.grid_row_start = grid_row_start
        #         self.grid_row_end = grid_row_end
        #         self.inner_html = ""

        #     def _to_style(self) -> str:
        #         return f"""
        #         .{self.class_} {{
        #         grid-column-start: {self.grid_column_start};
        #         grid-column-end: {self.grid_column_end};
        #         grid-row-start: {self.grid_row_start};
        #         grid-row-end: {self.grid_row_end};
        #         }}"""

        #     def text(self, text: str = ""):
        #         self.inner_html = text

        #     def markdown(self, text):
        #         self.inner_html = markdown.markdown(text)

        #     def to_html(self):
        #         return f"""<div class="box {self.class_}">{self.inner_html}</div>"""

        # class Grid:
        #     """A (CSS) Grid"""
        #     def __init__(
        #         self, template_columns="1 1 1", gap="10px", background_color="#fff", color="#444"
        #         ):
        #         self.template_columns = template_columns
        #         self.gap = gap
        #         self.background_color = background_color
        #         self.color = color
        #         self.cells: List[Cell] = []

        #     def __enter__(self):
        #         return self

        #     def __exit__(self, type, value, traceback):
        #         st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        #         st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        #         st.markdown(self._get_cells_html(), unsafe_allow_html=True)

        #     def _get_grid_style(self):
        #         return f"""
        #         <style>
        #             .wrapper {{
        #             display: grid;
        #             grid-template-columns: {self.template_columns};
        #             grid-gap: {self.gap};
        #             background-color: {self.background_color};
        #             color: {self.color};
        #             }}
        #             .box {{
        #             background-color: {self.color};
        #             color: {self.background_color};
        #             border-radius: 5px;
        #             padding: 20px;
        #             font-size: 150%;
        #             }}
        #             table {{
        #                 color: {self.color}
        #             }}
        #         </style>
        #         """
        #     def _get_cells_style(self):
        #         return (
        #             "<style>" + "\n".join([cell._to_style() for cell in self.cells]) + "</style>")

        #     def _get_cells_html(self):
        #         return (
        #             '<div class="wrapper">'
        #             + "\n".join([cell.to_html() for cell in self.cells])
        #             + "</div>")

        #     def cell(
        #         self,
        #         class_: str = None,
        #         grid_column_start: Optional[int] = None,
        #         grid_column_end: Optional[int] = None,
        #         grid_row_start: Optional[int] = None,
        #         grid_row_end: Optional[int] = None,
        #         ):
        #         cell = Cell(
        #             class_=class_,
        #             grid_column_start=grid_column_start,
        #             grid_column_end=grid_column_end,
        #             grid_row_start=grid_row_start,
        #             grid_row_end=grid_row_end,
        #             )
        #         self.cells.append(cell)
        #         return cell

        # # My preliminary idea of an API for generating a grid
        # with Grid("1 1 1") as grid:
        #     grid.cell(
        #     class_="a",
        #     grid_column_start=2,
        #     grid_column_end=3,
        #     grid_row_start=1,
        #     grid_row_end=2,
        #     )
        #     # .markdown("# This is A Markdown Cell")
        #     grid.cell("b", 2, 3, 2, 3).text("1")
        #     grid.cell("c", 3, 4, 2, 3).text("2")
        #     # grid.cell("d", 1, 2, 1, 3).text("3")
        #     # grid.cell("e", 3, 4, 1, 2).text("4")      



        


        

    

   

main()