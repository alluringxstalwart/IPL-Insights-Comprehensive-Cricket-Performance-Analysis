import pandas as pd


class ipldb:
    def __init__(self):
        self.df = pd.read_csv("./data/cleaned_ipl_2024_deliveries.csv")

    # Overall info
    def get_overall_info(self):
        return {
            "total_matches": self.df["match_no"].max(),
            "total_runs_scored": self.df["runs_of_bat"].sum(),
            "total_wickets": self.df[self.df["wicket_type"] != "NaN"][
                "wicket_type"
            ].count(),
            "total_extras": self.df["extras"].sum(),
            "orange_cap": "Virat Kohli",
            "purple_cap": "Harshal Patel",
            "champions": "Kolkata Knight Riders",
            "m_v_p": "Sunil Narine",
        }

    def get_all_players(self):
        return list(self.df["striker"].unique())

    # get all team names
    def get_all_teams(self):
        return list(self.df["batting_team"].unique())

    # get player player info : team name, total runs, batting average , strike rate , highest score, centuries, half centuries
    def get_player_info(self, player):
        team = self.df[self.df["striker"] == player]["batting_team"].iloc[0]

        total_runs = (
            self.df[self.df["striker"] == player]
            .groupby(["striker"])
            .agg(batting_run=("runs_of_bat", "sum"))
            .sort_values("batting_run", ascending=False)["batting_run"]
            .iloc[0]
        )

        batting_avg = round(
            total_runs
            / self.df[self.df["striker"] == player][self.df["wicket_type"] != "NaN"]
            .groupby("striker")
            .agg(out_innings=("wicket_type", "count"))["out_innings"]
            .values[0],
            2,
        )

        strike_rate = round(
            (
                total_runs
                / (
                    self.df[self.df["striker"] == player][
                        (self.df["wide"] == 0)
                        & (self.df["legbyes"] == 0)
                        & (self.df["byes"] == 0)
                        & (self.df["noballs"] == 0)
                    ].shape[0]
                )
            )
            * 100,
            2,
        )

        highest_score = (
            self.df[self.df["striker"] == player]
            .groupby("match_id")
            .agg(total_runs=("runs_of_bat", "sum"))["total_runs"]
            .max()
        )

        centuries = (
            self.df[self.df["striker"] == player]
            .groupby("match_id")
            .agg(total_runs=("runs_of_bat", "sum"))["total_runs"]
            >= 100
        ).sum()

        half_centuries = (
            self.df[self.df["striker"] == player]
            .groupby("match_id")
            .agg(total_runs=("runs_of_bat", "sum"))["total_runs"]
            >= 50
        ).sum()

        return {
            "team": team,
            "total_runs": total_runs,
            "batting_avg": batting_avg,
            "strike_rate": strike_rate,
            "highest_score": highest_score,
            "centuries": centuries,
            "half_centuries": half_centuries,
        }

    # get inning wise runs
    def get_player_inning_runs(self, player):
        temp_df = (
            self.df[self.df["striker"] == player]
            .groupby("match_no")
            .agg(total_runs=("runs_of_bat", "sum"), vs=("bowling_team", "max"))
            .reset_index()
        )
        temp_df["match_no"] = temp_df["match_no"].apply(lambda x: "Match " + str(x))
        return temp_df

    # get inning wise strike rate
    def get_player_inning_strike_rate(self, player):
        temp_df = round(
            (
                (
                    self.df[self.df["striker"] == player]
                    .groupby("match_no")
                    .agg(total_runs=("runs_of_bat", "sum"))["total_runs"]
                    / self.df[self.df["striker"] == player][
                        (self.df["wide"] == 0)
                        & (self.df["legbyes"] == 0)
                        & (self.df["byes"] == 0)
                        & (self.df["noballs"] == 0)
                    ]
                    .groupby("match_no")
                    .agg(balls_by_innings=("over", "count"))["balls_by_innings"]
                )
                * 100
            ),
            2,
        ).reset_index(name="strike_rate")
        temp_df["match_no"] = temp_df["match_no"].apply(lambda x: "Match " + str(x))
        return temp_df

    # get runs by venue
    def get_player_runs_by_venue(self, player):
        temp_df = (
            self.df[self.df["striker"] == player]
            .groupby("venue")
            .agg(total_runs=("runs_of_bat", "sum"))
            .reset_index()
        )
        temp_df["venue_name"] = temp_df["venue"].str.split(",").apply(lambda x: x[0])
        temp_df["venue"] = temp_df["venue"].str.split(",").apply(lambda x: x[-1])
        return temp_df

    # runs scored over the season by team
    def get_team_matchwise_info(self, team):
        temp_df = (
            self.df[self.df["batting_team"] == team]
            .groupby(["match_no"])
            .agg(
                batting_runs=("runs_of_bat", "sum"),
                extra_runs=("extras", "sum"),
                vs=("bowling_team", "max"),
                balls=("over", "count"),
                venue=("venue", "max"),
            )
            .reset_index()
        )
        temp_df["total_runs"] = temp_df["batting_runs"] + temp_df["extra_runs"]
        temp_df["run_rate"] = round((temp_df["total_runs"] / temp_df["balls"]) * 100, 2)
        temp_df["match_no_l"] = temp_df["match_no"].apply(lambda x: "Match " + str(x))
        temp_df["venue_name"] = temp_df["venue"].str.split(",").apply(lambda x: x[0])
        temp_df["venue"] = temp_df["venue"].str.split(",").apply(lambda x: x[-1])
        return temp_df
