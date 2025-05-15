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
        return f"Player(name={self.name}, position={self.position}, rank={self.pos_rank}, proj_points={self.proj_points}, bye={self.bye}, sort_index={self.sort_index})"



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
            raise ValueError(f"No players found at position: {position}")

        for player in self.player_map[position]:
            if player.name.lower() == name.lower():
                return player

        raise ValueError(f"Player '{name}' not found at position '{position}'.")


    def print_all_players(self):
        for position, queue in self.player_map.items():
            print(f"Position: {position}")
            for player in sorted(queue):
                print(f"  {player}")