import json
from datetime import timedelta
from datetime import datetime    
import requests 
from bs4 import BeautifulSoup 

file = open('connections.json')
connections = json.load(file)
file.close()
last_date = connections[-1]["date"]
start_date = datetime.strptime(last_date,"%Y-%m-%d").date()
start_date = start_date + timedelta(days=1)
start_id = connections[-1]["id"] + 1


new_connects = []
while start_date <= datetime.today().date():
    URL = f"https://connections.swellgarfo.com/nyt/{start_id}" 
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    script = soup.find_all('script')[13]
    connection = json.loads(script.string.strip())
    
    
    id = connection["props"]["pageProps"]["id"] 
    condate = start_date.strftime('%Y-%m-%d')
    print(f"Adding Connection #{id} from {condate}")
    descriptions = []
    words = []
    for answer in connection["props"]["pageProps"]["answers"]:
        descriptions.append(answer["description"])
        words.append(answer["words"])
        
    con_item = {"id":int(id),
                "date":condate,
                "answers": [
            {
                "category": "yellow",
                "connection": descriptions[0],
                "items": words[0]
            },
            {
                "category": "green",
                "connection": descriptions[1],
                "items": words[1]
            },
            {
                "category": "blue",
                "connection": descriptions[2],
                "items": words[2]
            },
            {
                "category": "purple",
                "connection": descriptions[3],
                "items": words[3]
            }
        ]}
    new_connects.append(con_item)
    start_date = start_date + timedelta(days=1)
    start_id += 1
    
    
file = open('connections.json')
connections = json.load(file)
file.close()

connections = connections + new_connects
with open('connections.json', 'w') as f:
        json.dump(connections, f, indent=4)
        file.close()
#print(connection_list)