from flask import request, jsonify
from players import PlayerOrganizer, Player

# Think this is good for now, basically just adds a given player either to your team or to the opposing team while also removing them from the organizer
def make_add_player_handler(organizer, user_team, opp_team):
    def add_player():
        name = request.args.get("name")
        position = request.args.get("position")
        user_str = request.args.get("user").lower()
        user = user_str == "true"

        player = organizer.remove_player_by_name(name, position)
        if player is None:
            return jsonify({"status": "failure", "message": "Player not found."}), 404
        
        if user:
            user_team[position] += 1
        else:
            opp_team.append(player)

        return jsonify({"status": "success", "message": f"{player.name} added."}), 200
    return add_player


# TODO: Need to modify so that you just retrieve a given player, not return next best player
def make_get_player_handler(organizer: PlayerOrganizer):
    def get_player():
        position = request.args.get("position")
        player = organizer.get_next_best_player(position)
        if player:
            return jsonify(player.__dict__), 200
        return jsonify({"message": "No player found for position."}), 404
    return get_player

# I think this one is fine for now, basically just returns all the players in the organizer
def make_fetch_all_players_handler(organizer: PlayerOrganizer):
    def fetch_all_players():
        all_players = {
            pos: [p.__dict__ for p in sorted(queue)]
            for pos, queue in organizer.player_map.items()
        }
        return jsonify(all_players), 200
    return fetch_all_players
    # This will return a dictionary with key values of positions. At each position is a heap where the players
    # are ordered py position rank. Each player object is converted into a dictionary with all of their corresponding
    # values, so all player information is accessible from the frontend
