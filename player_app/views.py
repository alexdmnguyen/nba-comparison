from django.shortcuts import render
from django.http import JsonResponse
from .scraper.scraper import get_random_players, get_all_players

def compare_players(request):
    player1 = None
    player2 = None
    error_message = None
    default_image_url = '/static/images/player.png'

    if request.method == "POST":
        # Handle form submission (search for specific players)
        player1_name = request.POST.get("player1_name", "").strip()
        player2_name = request.POST.get("player2_name", "").strip()

        if player1_name and player2_name:
            # Perform a search for the entered player names
            all_players = get_all_players()  # Fetch all players
            player1 = next((p for p in all_players if p['name'].lower() == player1_name.lower()), None)
            player2 = next((p for p in all_players if p['name'].lower() == player2_name.lower()), None)

            if not player1 or not player2:
                error_message = "One or both players not found. Please try again."
        else:
            # If no specific player search, get random players
            player1, player2 = get_random_players()

    else:
        # Initial page load: Get two random players to compare
        player1, player2 = get_random_players()

    # Set image URLs for the players
    if player1 and player2:
        player1['image_url'] = default_image_url
        player2['image_url'] = default_image_url

        player1['points_per_game'] = float(player1['points_per_game'])
        player2['points_per_game'] = float(player2['points_per_game'])
        player1['rebounds_per_game'] = float(player1['rebounds_per_game'])
        player2['rebounds_per_game'] = float(player2['rebounds_per_game'])
        player1['assists_per_game'] = float(player1['assists_per_game'])
        player2['assists_per_game'] = float(player2['assists_per_game'])
        player1['steals_per_game'] = float(player1['steals_per_game'])
        player2['steals_per_game'] = float(player2['steals_per_game'])
        player1['blocks_per_game'] = float(player1['blocks_per_game'])
        player2['blocks_per_game'] = float(player2['blocks_per_game'])

    context = {
        'player1': player1,
        'player2': player2,
        'error_message': error_message,
    }
    return render(request, 'player_app/compare_players.html', context)


def search_players(request):
    players = get_all_players()  # Fetch all players
    query = request.GET.get('query', '').strip().lower()  # Get the search query from the request

    filtered_players = []
    if query:
        # Filter players whose names contain the query string
        filtered_players = [
            player['name']  # Only return the player names as strings
            for player in players
            if query in player['name'].lower()
        ]

    return JsonResponse(filtered_players, safe=False)  # Return a JSON array of player names
