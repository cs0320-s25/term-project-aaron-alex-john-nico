import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
league_swid = os.getenv("SWID")
league_s2 = os.getenv("ESPN_S2")

from espn_api.football import League  

league = League(league_id=4572608, year=2024, espn_s2=league_s2, swid=league_swid) 

player_population = league.free_agents(size= 500)

from espn_api.football import League  

league = League(league_id=4572608, year=2024, espn_s2=league_s2, swid=league_swid)  # Replace with your league ID
