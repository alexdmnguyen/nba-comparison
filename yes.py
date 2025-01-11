import requests
from bs4 import BeautifulSoup
import random

url = 'https://www.basketball-reference.com/leagues/NBA_2023_per_game.html'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'id': 'per_game_stats'})
tbody = table.find('tbody')
rows = tbody.find_all('tr')

players = []
for row in rows:
    cells = row.find_all('td')
    
    # Skip rows without player data
    if len(cells) == 0:
        continue
    
    # Extract player statistics
    player_name_elem = cells[0].find('a')
    player_name = player_name_elem.text if player_name_elem else "N/A"
    
    points_per_game = cells[28].text.strip()
    rebounds_per_game = cells[21].text.strip()
    assists_per_game = cells[22].text.strip()
    steals_per_game = cells[23].text.strip()
    blocks_per_game = cells[24].text.strip()
    
    player_data = {
        'name': player_name,
        'points_per_game': points_per_game,
        'rebounds_per_game': rebounds_per_game,
        'assists_per_game': assists_per_game,
        'steals_per_game': steals_per_game,
        'blocks_per_game': blocks_per_game
    }
    
    players.append(player_data)

def compare_players():
    player1, player2 = random.sample(players, 2)
    
    print("Player 1:")
    print_player_stats(player1)
    
    print("Player 2:")
    print_player_stats(player2)

def print_player_stats(player):
    print(f"Name: {player['name']}")
    print(f"Points per game: {player['points_per_game']}")
    print(f"Rebounds per game: {player['rebounds_per_game']}")
    print(f"Assists per game: {player['assists_per_game']}")
    print(f"Steals per game: {player['steals_per_game']}")
    print(f"Blocks per game: {player['blocks_per_game']}")
    print()

# Call the compare_players function when the button is clicked
compare_players()
