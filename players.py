import data2024

from dataclasses import dataclass, field

'''
Dataclass that contains the 'player' object. 5 fields: name, position, position rank, bye week 
and their projected weekly avg. points. 
'''
@dataclass
class Player:
    name: str
    position: str
    pos_rank: int
    proj_points: float
    bye: int

    def __init__(self, name, position, pos_rank, proj_points, bye):
        self.name = name
        self.position = position
        self.pos_rank = pos_rank
        self.proj_points = proj_points
        self.bye = bye

#2024 data
bye_weeks = {
    "ARI": 11,
    "ATL": 12,
    "BAL": 14,
    "BUF": 12,
    "CAR": 11,
    "CHI": 7,
    "CIN": 12,
    "CLE": 10,
    "DAL": 7,
    "DEN": 14,
    "DET": 5,
    "GB": 10,
    "HOU": 14,
    "IND": 14,
    "JAX": 12,
    "KC": 6,
    "LV": 10,
    "LAC": 5,
    "LAR": 6,
    "MIA": 6,
    "MIN": 6,
    "NE": 14,
    "NO": 12,
    "NYG": 11,
    "NYJ": 12,
    "PHI": 5,
    "PIT": 9,
    "SF": 9,
    "SEA": 10,
    "TB": 11,
    "TEN": 5,
    "WAS": 14
}

#for now, I just took top 400 players to get a good sample size. We certainly shouldn't need any more,
#but we can definitely reduce the number
top_players = []
   
#player population calls for top 400 free agents in an empty 2025 league 
for player in data2024.player_population:
    person = Player(player.name, player.position, player.posRank, player.projected_avg_points, bye_weeks.get(player.proTeam))

    top_players.append(person)

#list comprehension to make lists of each top position, we can use these lists to make sorting easier
top_qbs = [p for p in top_players if p.position == "QB"]

print(len(top_qbs))

top_rbs = [p for p in top_players if p.position == "RB"]

top_wrs = [p for p in top_players if p.position == "WR"]

top_kickers = [p for p in top_players if p.position == "K"]

top_def = [p for p in top_players if p.position == "D/ST"]

top_tes = [p for p in top_players if p.position == "TE"]

print(len(top_rbs))
print(len(top_wrs))
#print(top_wrs)
print(len(top_kickers))
print(len(top_def))
#print(top_def)
print(len(top_tes))
print(len(top_kickers))

#print(top_players)
#Add fields: name, pos, posRank, proj. points

#incorporate bye weeks? Depends on algorithim but could add a bye-week field.
#We can do so by adding a field for player team, and then just calculate each team's bye week (shouldn't be horrible with only 32 teams)
#The nfl schedule apparently is released on may 14th, so for now I can use 2024 model
#and then sub out values with 2025 once released
