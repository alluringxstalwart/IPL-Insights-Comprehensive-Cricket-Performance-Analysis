import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
from db import ipldb

dbo = ipldb()


class Dashboard:
    def __init__(self):
        self.tab_names = [
            "Home",
            "Batting Performance",
            "Bowling Performance",
            "Match Analysis",
            "Player Analysis",
            "Trends & Patterns",
            "Overall Performance",
        ]
        self.tabs = st.tabs(self.tab_names)
        with self.tabs[0]:
            st.title("IPL 2024🏏")
            st.subheader("Welcome to the IPL Analysis Dashboard!")
            st.write(
                """ 📊 Analyze. Compare. Predict.

Dive into the world of the Indian Premier League with our comprehensive analysis dashboard. Whether you're a die-hard fan, a data enthusiast, or a cricket strategist, this dashboard offers you a treasure trove of statistics, trends, and insights.
                 """
            )
            st.write("")
            st.write("")
            st.write("")
            self.cols = st.columns(4)
            with self.cols[0]:
                st.metric(
                    "Total Matches Played",
                    500,
                )

            with self.cols[1]:
                st.metric(
                    "Total Runs Scored",
                    500,
                )

            with self.cols[2]:
                st.metric(
                    "Total Wickets Taken",
                    500,
                )

            with self.cols[3]:
                st.metric(
                    "Total Extras Conceded",
                    500,
                )

        # Batting Performance tab
        with self.tabs[1]:

            st.header(self.tab_names[1])

            self.tabs_1_tabs = st.tabs(["Players", "Teams"])

            # Players tab
            with self.tabs_1_tabs[0]:
                cols = st.columns([5, 1])
                with cols[1]:
                    self.selected_player = st.selectbox(
                        "Select Player", dbo.get_all_players()
                    )
                with cols[0]:
                    st.header(self.selected_player)
                    st.subheader(dbo.get_player_info(self.selected_player)["team"])
                st.write("")
                batting_player_info_cols = st.columns(6)
                with batting_player_info_cols[0]:
                    st.metric(
                        "Total Runs",
                        str(dbo.get_player_info(self.selected_player)["total_runs"]),
                    )
                with batting_player_info_cols[1]:
                    st.metric(
                        "Batting Average",
                        str(dbo.get_player_info(self.selected_player)["batting_avg"]),
                    )
                with batting_player_info_cols[2]:
                    st.metric(
                        "Strike Rate",
                        str(dbo.get_player_info(self.selected_player)["strike_rate"]),
                    )
                with batting_player_info_cols[3]:
                    st.metric(
                        "Highest Score",
                        str(dbo.get_player_info(self.selected_player)["highest_score"]),
                    )
                with batting_player_info_cols[4]:
                    st.metric(
                        "Centuries",
                        str(dbo.get_player_info(self.selected_player)["centuries"]),
                    )
                with batting_player_info_cols[5]:
                    st.metric(
                        "Half Centuries",
                        str(
                            dbo.get_player_info(self.selected_player)["half_centuries"]
                        ),
                    )

                st.write("")
                st.write("")

                cols = st.columns(2)

                with cols[0]:

                    # rusn scored over the season
                    st.plotly_chart(
                        px.line(
                            dbo.get_player_inning_runs(self.selected_player),
                            x="match_no",
                            y="total_runs",
                            markers=True,
                            labels={"match_no": "Match", "total_runs": "Score"},
                            hover_data={"vs": True},
                            title="Runs Scored Over the Season",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

                with cols[0]:

                    # strike rate over the season
                    st.plotly_chart(
                        px.line(
                            dbo.get_player_inning_strike_rate(self.selected_player),
                            x="match_no",
                            y="strike_rate",
                            markers=True,
                            labels={"match_no": "Match", "strike_rate": "Strike Rate"},
                            title="Strike Rate Over the Season",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

                with cols[1]:
                    # venue bar chart

                    st.plotly_chart(
                        px.bar(
                            dbo.get_player_runs_by_venue(self.selected_player),
                            x="venue",
                            y="total_runs",
                            labels={
                                "venue": "Venue",
                                "venue_name": "Stadium Name",
                                "total_runs": "Score",
                            },
                            hover_data={"venue_name": True},
                            title="Perfomance By Venue",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

            # Teams tab
            with self.tabs_1_tabs[1]:
                cols = st.columns([5, 1])
                with cols[1]:
                    self.selected_team = st.selectbox(
                        "Select Player", dbo.get_all_teams()
                    )
                with cols[0]:
                    st.header(self.selected_team)

                self.team_matchwise_info = dbo.get_team_matchwise_info(
                    self.selected_team
                )
                cols = st.columns(2)

                with cols[0]:
                    # runs scored over the season
                    st.plotly_chart(
                        px.line(
                            self.team_matchwise_info,
                            x="match_no_l",
                            y="total_runs",
                            markers=True,
                            labels={
                                "match_no_l": "Match",
                                "match_no": "Match",
                                "total_runs": "Runs",
                            },
                            hover_data={
                                "match_no_l": False,
                                "match_no": True,
                                "vs": True,
                            },
                            title="Runs Scored Over the Season",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

                with cols[1]:
                    # run rate over the season
                    st.plotly_chart(
                        px.line(
                            self.team_matchwise_info,
                            x="match_no_l",
                            y="run_rate",
                            markers=True,
                            labels={
                                "match_no_l": "Match",
                                "match_no": "Match",
                                "run_rate": "Run Rate",
                            },
                            hover_data={
                                "match_no_l": False,
                                "match_no": True,
                                "vs": True,
                            },
                            title="Run Rate Over the Season",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

                with cols[0]:
                    # performance by venue

                    st.plotly_chart(
                        px.bar(
                            self.team_matchwise_info,
                            x="venue",
                            y="total_runs",
                            labels={
                                "venue": "Venue",
                                "venue_name": "Stadium Name",
                                "total_runs": "Runs",
                            },
                            hover_data={"venue_name": True, "venue": False, "vs": True},
                            title="Performance By Venue",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )

                with cols[1]:
                    #Performance by Opposition

                    st.plotly_chart(
                        px.bar(
                            self.team_matchwise_info,
                            x="vs",
                            y="total_runs",
                            labels={
                                'vs':'Opposition',
                                "total_runs": "Runs",
                            },
                            title="Performance By Opposition",
                        ).update_layout(
                            width=600,  # Adjust the width
                            height=400,  # Adjust the height
                            margin=dict(l=20, r=20, t=20, b=20),  # Minimize margins
                            legend=dict(
                                x=0.01, y=0.99, title="", orientation="h"
                            ),  # Adjust legend position and orientation
                        )
                    )



        with self.tabs[2]:

            st.header(self.tab_names[2])

        with self.tabs[3]:

            st.header(self.tab_names[3])

        with self.tabs[4]:

            st.header(self.tab_names[4])

        with self.tabs[5]:

            st.header(self.tab_names[5])

        with self.tabs[6]:

            st.header(self.tab_names[6])


Dashboard()
