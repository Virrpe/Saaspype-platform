import requests
response = requests.get('http://127.0.0.1:8002/api/chat/demo/ideas')
data = response.json()
print(f'Total ideas: {data["total"]}')
for i, idea in enumerate(data['ideas'], 1):
    print(f'{i}. {idea["title"]} ({idea["category"]})') 