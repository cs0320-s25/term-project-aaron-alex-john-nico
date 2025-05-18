import json
import os
from collections import defaultdict, Counter

# Define roster requirements
ROSTER_LIMIT = 16
POSITION_REQUIREMENTS = {
    'QB': {'min': 1, 'max': 3},
    'RB': {'min': 2, 'max': 4},
    'WR': {'min': 2, 'max': 4},
    'TE': {'min': 1, 'max': 2},
    'K': {'min': 1, 'max': 2},
    'DST': {'min': 1, 'max': 2},
    'FLEX': {'min': 1, 'max': 1},  # FLEX is a required position
}

FLEX_ELIGIBLE = {'RB', 'WR', 'TE'}

def requirements_met(roster):
    """
    Checks if the roster meets the specified positional requirements and constraints.
    """
    if len(roster) != ROSTER_LIMIT:
        return False
    # Count by 'position' as stored in the roster
    position_counts = Counter(player['position'] for player in roster)
    for position, limits in POSITION_REQUIREMENTS.items():
        count = position_counts.get(position, 0)
        if count < limits['min'] or count > limits['max']:
            return False
    return True

def calculate_player_scores(standings):
    """
    Calculate adjusted scores for each player based on projected points, positional needs,
    team composition, and penalties. Also ensures that the same player isn't added twice.
    """
    player_scores = {}
    roster = []
    team_counts = defaultdict(int)
    position_counts = defaultdict(int)
    selected_names = set()  # Tracks names of players already added

    # Flatten the standings dictionary into a list of players
    all_players = []
    for position, players in standings.items():
        for player in players:
            name, projected_points, team = player
            all_players.append({
                'name': name,
                'position': position,
                'projected_points': projected_points,
                'team': team
            })

    # Sort players by projected points descending
    all_players.sort(key=lambda x: x['projected_points'], reverse=True)

    for player in all_players:
        name = player['name']
        position = player['position']
        projected_points = player['projected_points']
        team = player['team']

        # Skip if the player is already in the roster
        if name in selected_names:
            continue

        # Skip if roster is full
        if len(roster) >= ROSTER_LIMIT:
            break

        # Skip positions not defined in requirements
        if position not in POSITION_REQUIREMENTS:
            continue

        # Determine if position requirement is needed
        position_needed = False
        if position_counts[position] < POSITION_REQUIREMENTS[position]['min']:
            position_needed = True
        elif position_counts[position] >= POSITION_REQUIREMENTS[position]['max']:
            continue  # Skip if max limit reached

        # Calculate adjusted score
        adjusted_score = projected_points
        if position_needed:
            adjusted_score += 50  # Bonus for filling required position
        if team_counts[team] > 0:
            adjusted_score -= 80  # Penalty for same team players
        if position_counts[position] >= POSITION_REQUIREMENTS[position]['max']:
            adjusted_score -= 150  # Penalty for exceeding max position limit

        # Add player to roster if not already added
        roster.append({
            'name': name,
            'position': position,
            'projected_points': projected_points,
            'adjusted_score': adjusted_score,
            'team': team
        })
        selected_names.add(name)
        position_counts[position] += 1
        team_counts[team] += 1
        player_scores[name] = adjusted_score

    # Ensure mandatory positions are filled after max limits
    mandatory_positions = ['K', 'DST', 'TE']
    for mandatory_position in mandatory_positions:
        if position_counts[mandatory_position] < POSITION_REQUIREMENTS[mandatory_position]['min']:
            # Find the next available player for the mandatory position
            for player in all_players:
                if (player['position'] == mandatory_position 
                    and player['name'] not in selected_names):
                    roster.append({
                        'name': player['name'],
                        'position': player['position'],
                        'projected_points': player['projected_points'],
                        'adjusted_score': player['projected_points'],
                        'team': player['team']
                    })
                    selected_names.add(player['name'])
                    position_counts[mandatory_position] += 1
                    team_counts[player['team']] += 1
                    player_scores[player['name']] = player['projected_points']
                    break

    # Add FLEX position if needed, ensuring no duplicate
    if position_counts['FLEX'] < POSITION_REQUIREMENTS['FLEX']['min']:
        for player in all_players:
            if (player['position'] in FLEX_ELIGIBLE 
                and player['name'] not in selected_names):
                roster.append({
                    'name': player['name'],
                    'position': 'FLEX',
                    'projected_points': player['projected_points'],
                    'adjusted_score': player['projected_points'],
                    'team': player['team']
                })
                selected_names.add(player['name'])
                position_counts['FLEX'] += 1
                team_counts[player['team']] += 1
                player_scores[player['name']] = player['projected_points']
                break

    # Verify if the constructed roster meets all requirements
    if not requirements_met(roster):
        print("Constructed roster does not meet all requirements. Saving roster anyway.")

    return player_scores, roster

def save_roster_to_json(roster, filename='optimized_roster.json'):
    """
    Save the roster to a JSON file. If the file doesn't exist, create it.
    """
    with open(filename, 'w') as f:
        json.dump(roster, f, indent=4)
    print(f"Roster saved to {filename}")

def add_dst_rankings(standings):
    """
    Adds hardcoded DST rankings to the standings dictionary.
    """
    dst_teams = [
        'Den', 'Hou', 'Phi', 'Bal', 'Min', 'Det', 'Sea', 'Gre', 'Dal', 'Buf',
        'Kan', 'Cle', 'LAC', 'NYG', 'Ari', 'LAR', 'Pit', 'Ind', 'Chi', 'SF',
        'Mia', 'NYJ', 'TB', 'Was', 'NE', 'JAX', 'LV', 'ATL', 'CIN', 'CAR',
        'NO', 'TEN'
    ]
    dst_players = []
    points = 33
    for team in dst_teams:
        dst_players.append([team + ' DST', points, team])
        points -= 1
    standings['DST'] = dst_players
    return standings

# Example usage
if __name__ == "__main__":
    # Load standings from a JSON file
    with open('final_standings.json', 'r') as f:
        standings = json.load(f)

    # Add hardcoded DST rankings
    standings = add_dst_rankings(standings)

    player_scores, roster = calculate_player_scores(standings)
    # Save the roster regardless of whether all requirements are met
    save_roster_to_json(roster)
