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
    # Count players by their "position" field (for FLEX the value is "FLEX")
    position_counts = Counter(player['position'] for player in roster)
    for position, limits in POSITION_REQUIREMENTS.items():
        count = position_counts.get(position, 0)
        if count < limits['min'] or count > limits['max']:
            return False
    return True

def calculate_player_scores(standings):
    """
    Calculates adjusted scores for each player and builds the roster.
    A set is used to ensure no duplicate players are added.
    After constructing the roster, it is sorted by adjusted_score (descending)
    and trimmed to exactly ROSTER_LIMIT players.
    """
    player_scores = {}
    roster = []
    team_counts = defaultdict(int)
    position_counts = defaultdict(int)
    selected_names = set()  # Tracks names already added

    # Flatten the standings dictionary into a list of players.
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

    # Sort players by projected points descending.
    all_players.sort(key=lambda x: x['projected_points'], reverse=True)

    # Main loop: add players while roster < ROSTER_LIMIT.
    for player in all_players:
        name = player['name']
        position = player['position']
        projected_points = player['projected_points']
        team = player['team']

        if name in selected_names:
            continue
        if len(roster) >= ROSTER_LIMIT:
            break
        if position not in POSITION_REQUIREMENTS:
            continue

        # Do not exceed the positional maximum.
        if position_counts[position] >= POSITION_REQUIREMENTS[position]['max']:
            continue

        # Calculate adjusted score. Add bonus if the minimum for the position has not been met,
        # and subtract a penalty if the same team is already represented.
        adjusted_score = projected_points
        if position_counts[position] < POSITION_REQUIREMENTS[position]['min']:
            adjusted_score += 50  # bonus for filling a required slot
        if team_counts[team] > 0:
            adjusted_score -= 80  # penalty for duplicate team

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

    # Ensure mandatory positions are filled if missing.
    mandatory_positions = ['K', 'DST', 'TE']
    for pos in mandatory_positions:
        if position_counts[pos] < POSITION_REQUIREMENTS[pos]['min']:
            for player in all_players:
                if player['position'] == pos and player['name'] not in selected_names:
                    roster.append({
                        'name': player['name'],
                        'position': pos,
                        'projected_points': player['projected_points'],
                        'adjusted_score': player['projected_points'],  # no bonus applied here
                        'team': player['team']
                    })
                    selected_names.add(player['name'])
                    position_counts[pos] += 1
                    team_counts[player['team']] += 1
                    player_scores[player['name']] = player['projected_points']
                    break

    # Add FLEX position if needed.
    if position_counts['FLEX'] < POSITION_REQUIREMENTS['FLEX']['min']:
        for player in all_players:
            if player['position'] in FLEX_ELIGIBLE and player['name'] not in selected_names:
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

    # Final sorting and trimming.
    roster = sorted(roster, key=lambda player: player['adjusted_score'], reverse=True)
    if len(roster) > ROSTER_LIMIT:
        roster = roster[:ROSTER_LIMIT]

    if not requirements_met(roster):
        print("Constructed roster does not meet all requirements. Saving roster anyway.")

    return player_scores, roster

def save_roster_to_json(roster, filename='optimized_roster.json'):
    """
    Save the roster to a JSON file.
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

if __name__ == "__main__":
    # Load standings from a JSON file.
    with open('final_standings.json', 'r') as f:
        standings = json.load(f)

    # Add hardcoded DST rankings
    standings = add_dst_rankings(standings)

    player_scores, roster = calculate_player_scores(standings)
    print(roster)
    save_roster_to_json(roster)
