import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables from .env file
load_dotenv()

# API Key를 환경 변수에서 가져오기
api_key = os.getenv('PUBG_API_KEY')

def get_pubg_data(player_name, season_id='division.bro.official.pc-2018-30'):
    encoded_player_name = quote(player_name)  # 플레이어 이름 인코딩
    url = f'https://api.pubg.com/shards/steam/players?filter[playerNames]={encoded_player_name}'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/vnd.api+json'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"Requesting player data for: {player_name}")
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        player_id = data['data'][0]['id']
        season_url = f'https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season_id}/ranked'
        season_response = requests.get(season_url, headers=headers)
        
        print(f"Requesting season data for player ID: {player_id}")
        print(f"Season Response Status Code: {season_response.status_code}")
        
        if season_response.status_code == 200:
            season_data = season_response.json()
            stats = season_data['data']['attributes']['rankedGameModeStats']['squad']
            rank_points = stats['currentRankPoint']  # 랭크 포인트 정보
            print(f"Player {player_name} rank points: {rank_points}")
            return rank_points
        else:
            print(f"Failed to retrieve season data: {season_response.status_code}")
    elif response.status_code == 404:
        print(f"Player '{player_name}' not found.")
    else:
        print(f"Failed to retrieve player data: {response.status_code}")
    
    return None

# 테스트 실행
if __name__ == "__main__":
    player_name = "SSIB_Onbo"
    rank_points = get_pubg_data(player_name)
    if rank_points is not None:
        print(f"Player {player_name} has {rank_points} rank points.")
    else:
        print(f"Could not retrieve rank points for player {player_name}.")
