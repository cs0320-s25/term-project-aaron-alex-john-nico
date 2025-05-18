import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import json
"""
pip install pandas
pip install numpy
pip install -U scikit-learn
pip install matplotlib     
"""


# Load Data
data = pd.read_csv('projection/2015-24_seasonal_data.csv')

# Preprocess Data
data.fillna(0, inplace=True)

# Ensure all position values are strings
data['position'] = data['position'].astype(str)

# Encode Categorical Data
label_enc_position = LabelEncoder()
label_enc_name = LabelEncoder()
data['position_encoded'] = label_enc_position.fit_transform(data['position'])
data['player_display_name_encoded'] = label_enc_name.fit_transform(data['player_display_name'])

# Save original labels for reference
original_positions = data['position']
original_names = data['player_display_name']

# If 'team' column exists, save it; otherwise, use 'Unknown'
if 'team' in data.columns:
    original_teams = data['team']
else:
    original_teams = pd.Series(['Unknown'] * len(data))

# Drop non-numeric columns not needed for modeling
data = data.drop(columns=['player_id', 'position', 'player_display_name', 'team'], errors='ignore')

# Select Features and Target
X = data.drop(columns=['fantasy_points_ppr'])
y = data['fantasy_points_ppr']

# Train-Test Split
X_train, X_test, y_train, y_test, pos_train, pos_test, name_train, name_test, team_train, team_test = train_test_split(
    X, y, original_positions, original_names, original_teams, test_size=0.2, random_state=42
)

# Scaling Features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model Training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2 Score:', r2_score(y_test, y_pred))

# Map back to DataFrame for easy analysis
results = pd.DataFrame(X_test, columns=X.columns)
results['predicted_points'] = y_pred
results['position'] = pos_test.values
results['player_display_name'] = name_test.values
results['team'] = team_test.values

# Display top 3 scorers per position
for position in results['position'].unique():
    top_scorers = results[results['position'] == position].nlargest(3, 'predicted_points')
    print(f"Position: {position}")
    print(top_scorers[['player_display_name', 'predicted_points']])

# Plot: Actual vs. Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
plt.title('Actual vs. Predicted Fantasy Points')
plt.xlabel('Actual Fantasy Points')
plt.ylabel('Predicted Fantasy Points')
plt.grid(True)
plt.show()

if False:
    # Export to JSON by position
    for position in results['position'].unique():
        position_group = results[results['position'] == position]
        players_data = position_group[['player_display_name', 'predicted_points']].to_dict(orient='records')
        filename = f"{position}_rank.json"
        with open(filename, 'w') as f:
            json.dump(players_data, f, indent=4)
        print(f"Data for position '{position}' has been saved to '{filename}'.")

def final_standings_players(results_df, supplementary_file='Projection/12-21FantasyData.csv'):
    """
    Returns a dictionary with positions as keys and a list of all players as values.
    Each player is represented as a tuple: (player_display_name, predicted_points, team).
    If a player's team is 'Unknown', the function attempts to update it using the supplementary data.

    Parameters:
    - results_df (pd.DataFrame): DataFrame containing 'position', 'player_display_name', 'predicted_points', and 'team' columns.
    - supplementary_file (str): Path to the CSV file containing supplementary player-team data.

    Returns:
    - dict: Dictionary with positions as keys and list of player tuples as values, sorted by predicted_points descending.
    """
    # Load the supplementary data
    try:
        supplementary_data = pd.read_csv(supplementary_file)
    except FileNotFoundError:
        print(f"Supplementary file '{supplementary_file}' not found.")
        return {}

    # Create a mapping from player names to teams
    player_team_mapping = supplementary_data.set_index('Player')['Tm'].to_dict()

    # Update 'Unknown' teams using the supplementary data
    results_df['team'] = results_df.apply(
        lambda row: player_team_mapping.get(row['player_display_name'], row['team']) if row['team'] == 'Unknown' else row['team'],
        axis=1
    )

    # Build the standings dictionary
    standings = {}
    for position in results_df['position'].unique():
        players = (
            results_df[results_df['position'] == position]
            .sort_values(by='predicted_points', ascending=False)
            [['player_display_name', 'predicted_points', 'team']]
            .values.tolist()
        )
        standings[position] = players

    return standings
def turn_to_json(standings_dict, output_filename='final_standings.json'):
    """
    Converts the standings dictionary into a JSON file.

    Parameters:
    - standings_dict (dict): Dictionary with positions as keys and list of player tuples as values.
    - output_filename (str): Name of the output JSON file.

    Returns:
    - None
    """
    try:
        with open(output_filename, 'w') as json_file:
            json.dump(standings_dict, json_file, indent=4)
        print(f"Standings have been successfully written to '{output_filename}'.")
    except Exception as e:
        print(f"An error occurred while writing to JSON: {e}")

standings = final_standings_players(results)
print(standings)
turn_to_json(standings)

