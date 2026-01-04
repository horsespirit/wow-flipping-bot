import requests
import os

def login_e_analizza():
    # Recupera i dati dai segreti di GitHub
    email = os.getenv('FP_EMAIL')
    password = os.getenv('FP_PASSWORD')
    
    login_url = "https://api.flippingpal.com/auth/login"
    market_url = "https://api.flippingpal.com/retail/market/ah-data-undercut/eu"
    
    print("Tentativo di login automatico...")
    try:
        login_res = requests.post(login_url, json={"email": email, "password": password})
        login_data = login_res.json()
        
        token = "Bearer " + login_data.get('accessToken')
        user_id = login_data.get('user', {}).get('id')
        headers = {'authorization': token, 'user-agent': 'Mozilla/5.0'}
        
        # Lista dei tuoi server
        realms = [3679,1325,3713,1104,3686,512,1302,3702,578,1406,1597,1417,580,581,1416,1393,1307,1127,1084,531,1618,1121,1403,1092,1378,3691,1315,1091,3692,1385,3703,509,1401,3657,1303,1587,1390,1596,1305,1080,3690,633,1082,1388,570,3681,1098,1621,1085,1624,1105,612,1316,3696,1408,1301,1309,1396,3682,1329,1099,1096,3666,1598,3391,3656,2073,1331,2074,604,1405,1402,3674,1384,1122,1400,510,1313,1097,1335,1379]
        
        print("Login OK! Scarico dati...")
        r = requests.post(market_url, headers=headers, json={"retailSellingRealms": realms, "retailBuyingRealms": realms, "userId": user_id}, timeout=600)
        data = r.json()

        # Creazione della Dashboard
        categorie = ["Weapon", "Armor", "Container", "Consumable", "Glyph", "Trade Goods", "Recipe", "Gem", "Miscellaneous", "Quest", "Hollow"]
        html = "<html><head><style>body{font-family:Arial;background:#121212;color:white} .cat-box{border:1px solid #444;margin:10px;padding:15px;border-radius:8px} .buy{color:#4caf50} .sell{color:#f44336} table{width:100%}</style></head><body>"
        html += "<h1>Dashboard Strategica WoW (Aggiornamento Automatico)</h1>"

        for cat in categorie:
            items = [i for i in data if isinstance(i, dict) and i.get('category') == cat]
            if not items: continue
            
            srv_prices = {}
            for i in items:
                s = i.get('realmId'); p = i.get('price', 0)
                if s not in srv_prices: srv_prices[s] = []
                srv_prices[s].append(p)
            
            # Analisi prezzi medi per server
            sorted_srv = sorted({s: sum(p)/len(p) for s, p in srv_prices.items()}.items(), key=lambda x: x[1])
            
            html += f"<div class='cat-box'><h2>Categoria: {cat}</h2><table><tr>"
            html += f"<td valign='top'><b>Top 10 ACQUISTO</b><br>"
            for s, p in sorted_srv[:10]: html += f"<span class='buy'>Server {s}</span> ({round(p/10000)}g)<br>"
            html += f"</td><td valign='top'><b>Top 5 VENDITA</b><br>"
            for s, p in sorted_srv[-5:]: html += f"<span class='sell'>Server {s}</span> ({round(p/10000)}g)<br>"
            html += "</td></tr></table></div>"

        html += "</body></html>"
        with open("index.html", "w") as f: f.write(html)
        print("Sito web creato correttamente!")

    except Exception as e:
        print(f"Errore fatale: {e}")

if __name__ == "__main__":
    login_e_analizza()
 
