import requests
from bs4 import BeautifulSoup
import random

def get_random_players():
    url = 'https://www.basketball-reference.com/leagues/NBA_2025_per_game.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'id': 'per_game_stats'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    players = []
    player_names = set()

    for row in rows:
        cells = row.find_all('td')

        # Skip rows without player data
        if len(cells) == 0:
            continue

        player_name_elem = cells[0].find('a')
        player_name = player_name_elem.text if player_name_elem else "N/A"

        # Skip player if already added
        if player_name in player_names:
            continue

        player_names.add(player_name)

        # Handling team extraction
        team_elem = cells[2]
        teams = extract_teams(team_elem)

        # Extract stats, defaulting to "0" if missing
        points_per_game = extract_stat(cells[28])
        rebounds_per_game = extract_stat(cells[22])
        assists_per_game = extract_stat(cells[23])
        steals_per_game = extract_stat(cells[24])
        blocks_per_game = extract_stat(cells[25])

        player_data = {
            'name': player_name,
            'team': ', '.join(teams) if len(teams) > 1 else teams[0],
            'points_per_game': points_per_game,
            'rebounds_per_game': rebounds_per_game,
            'assists_per_game': assists_per_game,
            'steals_per_game': steals_per_game,
            'blocks_per_game': blocks_per_game
        }

        players.append(player_data)

    player1 = random.choice(players)
    player2 = random.choice(players)

    while player2['name'] == player1['name']:
        player2 = random.choice(players)

    return player1, player2

def extract_teams(team_elem):
    """Extracts teams from a team element"""
    if team_elem.text.strip() == "TOT":
        teams = []
        for sibling in team_elem.next_siblings:
            if sibling.name == 'td':
                break
            if sibling.name == 'a':
                teams.append(sibling.text.strip())
        return teams if teams else ["N/A"]
    else:
        return [team_elem.text.strip()]


def extract_stat(cell):
    """Extracts player stat, defaults to '0' if the stat is missing"""
    return cell.text.strip() if cell else "0"

def get_all_players():
    url = 'https://www.basketball-reference.com/leagues/NBA_2025_per_game.html'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'per_game_stats'})
    tbody = table.find('tbody')
    rows = tbody.find_all('tr')

    players = []

    for row in rows:
        cells = row.find_all('td')

        if len(cells) == 0:  # Skip empty rows
            continue

        player_name_elem = cells[0].find('a')
        player_name = player_name_elem.text if player_name_elem else "N/A"

        # Extracting the team info
        team_elem = cells[2]
        team = team_elem.text.strip() if team_elem else "N/A"

        # Extracting stats
        points_per_game = extract_stat(cells[28])
        rebounds_per_game = extract_stat(cells[22])
        assists_per_game = extract_stat(cells[23])
        steals_per_game = extract_stat(cells[24])
        blocks_per_game = extract_stat(cells[25])

        players.append({
            'name': player_name,
            'team': team,
            'points_per_game': points_per_game,
            'rebounds_per_game': rebounds_per_game,
            'assists_per_game': assists_per_game,
            'steals_per_game': steals_per_game,
            'blocks_per_game': blocks_per_game
        })

    return players
