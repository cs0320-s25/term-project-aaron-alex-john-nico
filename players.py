import data2024
import heapq
from collections import defaultdict
from dataclasses import dataclass, field

'''
Dataclass that contains the 'player' object. 5 fields: name, position, position rank, bye week 
and their projected weekly avg. points. 
'''
# Full-featured Player class
@dataclass(order=True)
class Player:
    sort_index: int = field(init=False, repr=False)
    pos_rank: int
    name: str
    position: str
    proj_points: float
    bye: int

    def __post_init__(self):
        self.sort_index = self.pos_rank  # heapq will sort by pos_rank by default

    def __repr__(self):
        return f"Player(name={self.name}, position={self.position}, rank={self.pos_rank})"



# Organizer that stores players by position in priority queues
class PlayerOrganizer:
    def __init__(self):
        self.player_map = defaultdict(list)  # Maps position to a heap

    def add_player(self, player: Player):
        heapq.heappush(self.player_map[player.position], player)

    def get_next_best_player(self, position: str):
        queue = self.player_map.get(position)
        if queue:
            return queue[0]  # Peek
        return None

    def poll_next_best_player(self, position: str):
        queue = self.player_map.get(position)
        if queue:
            return heapq.heappop(queue)  # Remove and return
        return None

    def is_position_empty(self, position: str):
        return not self.player_map.get(position)
    
    def remove_player_by_name(self, name: str, position: str):
        queue = self.player_map.get(position)
        if not queue:
            raise ValueError(f"No players found at position: {position}")

        found = False
        new_queue = []
        removed_player = None

        while queue:
            player = heapq.heappop(queue)
            if player.name == name:
                found = True
                removed_player = player
                continue
            new_queue.append(player)

        if not found:
            raise ValueError(f"Player '{name}' not found at position '{position}'.")

        heapq.heapify(new_queue)
        self.player_map[position] = new_queue

        return removed_player
    
    def get_player_by_name(self, position: str, name: str):
        """
        Returns a player object matching the given name and position.
        Does not remove the player from the organizer.
        Returns None if the position or player is not found.
        """
        if position not in self.player_map:
            print(f"Position '{position}' not found in player_map.")
            return None

        for player in self.player_map[position]:
            if player.name.lower() == name.lower():
                return player

        print(f"Player with name '{name}' not found in position '{position}'.")
        return None


    def print_all_players(self):
        for position, queue in self.player_map.items():
            print(f"Position: {position}")
            for player in sorted(queue):
                print(f"  {player}")


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
