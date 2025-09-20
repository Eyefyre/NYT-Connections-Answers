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

URL = f"https://www.nytimes.com/svc/connections/v2/{con_date}.json" 
r = requests.get(URL)
content = json.loads(r.content)
print(f"Adding Connection #{id} from {con_date}")
groups = []
for group in content["categories"]:
    categ = {"level":-1,"group":group["title"],"members":[]}
    for member in group["cards"]:
        categ["members"].append(member["content"])
    groups.append(categ)

    
con_item = {"id":int(id),"date":con_date,"answers": groups}
connections.append(con_item)
    
with open('connections.json', 'w') as f:
        json.dump(connections, f, indent=4)
        f.close()

