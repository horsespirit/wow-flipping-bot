import requests
import json

def analizza_e_crea_web():
    url = "https://api.flippingpal.com/retail/market/ah-data-undercut/eu"
    headers = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2OTRmOGYxZjFlNmI0MTM3ZTQ2ODMwY2UiLCJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzY3NTA4NDAwLCJleHAiOjE3Njc1MTIwMDB9.DIJmaM9wMVCC1-YJFpy50SiCO0UyWPXhN42EIaM_Ynk',
        'user-agent': 'Mozilla/5.0'
    }
    realms = [3679,1325,3713,1104,3686,512,1302,3702,578,1406,1597,1417,580,581,1416,1393,1307,1127,1084,531,1618,1121,1403,1092,1378,3691,1315,1091,3692,1385,3703,509,1401,3657,1303,1587,1390,1596,1305,1080,3690,633,1082,1388,570,3681,1098,1621,1085,1624,1105,612,1316,3696,1408,1301,1309,1396,3682,1329,1099,1096,3666,1598,3391,3656,2073,1331,2074,604,1405,1402,3674,1384,1122,1400,510,1313,1097,1335,1379]
    
    r = requests.post(url, headers=headers, json={"retailSellingRealms": realms, "retailBuyingRealms": realms, "userId": "694f8f1f1e6b4137e46830ce"}, timeout=600)
    data = r.json()
    
    categorie = ["Weapon", "Armor", "Container", "Consumable", "Glyph", "Trade Goods", "Recipe", "Gem", "Miscellaneous", "Quest", "Hollow"]
    html_content = "<html><head><title>WoW Market Dashboard</title><style>body{font-family:sans-serif;background:#1a1a1a;color:white;padding:20px} table{width:100%;margin-bottom:40px;border-collapse:collapse} th,td{border:1px solid #444;padding:10px;text-align:left} th{background:#333} .buy{color:#4caf50} .sell{color:#f44336}</style></head><body><h1>Dashboard Mercato WoW</h1>"

    for cat in categorie:
        items = [i for i in data if i.get('category') == cat]
        if not items: continue
        
        prezzi_server = {}
        for i in items:
            s_id = i.get('realmId'); prezzo = i.get('price', 0)
            if s_id not in prezzi_server: prezzi_server[s_id] = []
            prezzi_server[s_id].append(prezzo)
        
        media = sorted({s: sum(p)/len(p) for s, p in prezzi_server.items()}.items(), key=lambda x: x[1])
        
        html_content += f"<h2>Categoria: {cat}</h2>"
        html_content += "<table><tr><th>Top 10 ACQUISTO (Economici)</th><th>Top 5 VENDITA (Cari)</th></tr><tr><td>"
        for s, p in media[:10]: html_content += f"<div class='buy'>Server {s}: {round(p/10000, 2)}g</div>"
        html_content += "</td><td>"
        for s, p in media[-5:]: html_content += f"<div class='sell'>Server {s}: {round(p/10000, 2)}g</div>"
        html_content += "</td></tr></table>"

    html_content += "</body></html>"
    with open("index.html", "w") as f: f.write(html_content)

if __name__ == "__main__":
    analizza_e_crea_web()
