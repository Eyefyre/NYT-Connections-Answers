import json
from datetime import datetime    
import requests

file = open('connections.json')
connections = json.load(file)
file.close()


id = connections[-1]["id"] + 1
con_date = datetime.today().strftime('%Y-%m-%d')
if connections[-1]["date"] == con_date:
    print(f"Connection #{id-1} from {con_date} already exists in file, exiting")
    exit()

URL = f"https://www.nytimes.com/svc/connections/v1/{con_date}.json" 
r = requests.get(URL)

content = json.loads(r.content)
print(f"Adding Connection #{id} from {con_date}")
groups = []
for group in content["groups"]:
    categ = {"level":content["groups"][group]["level"],"group":group,"members":content["groups"][group]["members"]}
    groups.append(categ)

    
con_item = {"id":int(id),"date":con_date,"answers": groups}
connections.append(con_item)
    
with open('connections.json', 'w') as f:
        json.dump(connections, f, indent=4)
        f.close()
