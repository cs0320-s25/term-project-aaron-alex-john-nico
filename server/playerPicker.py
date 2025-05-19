import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import os
from dotenv import load_dotenv
from espn_api.football import League  

# Load environment variables
load_dotenv()
league_swid = os.getenv("SWID")
league_s2 = os.getenv("ESPN_S2")

# Fetch free agent data from ESPN
league = League(league_id=4572608, year=2024, espn_s2=league_s2, swid=league_swid) 
espn_free_agents = {player.name: player.proTeam for player in league.free_agents(size=500)}

# Load Data
data = pd.read_csv('server/2015-24_seasonal_data.csv')

# Filter data for the 2024 season
data = data[data['season'] == 2024]

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
original_teams = data['team'] if 'team' in data.columns else pd.Series(['Unknown'] * len(data))

# Update "Unknown" teams using ESPN free agents data
updated_teams = [
    espn_free_agents.get(name, team) for name, team in zip(original_names, original_teams)
]

# Drop non-numeric columns not needed for modeling
data_model = data.drop(columns=['player_id', 'position', 'player_display_name', 'team'], errors='ignore')

# Select Features and Target
X = data_model.drop(columns=['fantasy_points_ppr'])
y = data_model['fantasy_points_ppr']

# Train-Test Split
X_train, X_test, y_train, y_test, pos_train, pos_test, name_train, name_test, team_train, team_test = train_test_split(
    X, y, original_positions, original_names, updated_teams, test_size=0.2, random_state=42
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
results['team'] = pd.Series(team_test)
results['season'] = 2024  # Since we've filtered for 2024, we can assign this directly

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

# Function to build final standings
def final_standings_players(results_df):
    """
    Returns a dictionary with positions as keys and a list of all players as values.
    Each player is represented as a tuple: (player_display_name, predicted_points, team).
    """
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

# Function to save standings to JSON
def turn_to_json(standings_dict, output_filename='final_standings.json'):
    """
    Converts the standings dictionary into a JSON file.
    """
    try:
        with open(output_filename, 'w') as json_file:
            json.dump(standings_dict, json_file, indent=4)
        print(f"Standings have been successfully written to '{output_filename}'.")
    except Exception as e:
        print(f"An error occurred while writing to JSON: {e}")

# Generate and save standings
#standings = final_standings_players(results)
#turn_to_json(standings)
print(data)
