import os
import requests
import json

def login_e_analizza():
    # Recupero credenziali dai segreti di GitHub
    email = os.getenv('FP_EMAIL')
    password = os.getenv('FP_PASSWORD')
    
    # Lista di possibili indirizzi API per il login
    login_urls = [
        "https://api.flippingpal.com/auth/login",
        "https://api.flippingpal.com/v1/auth/login",
        "https://api.flippingpal.com/api/auth/login"
    ]
    
    headers_base = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://flippingpal.com',
        'Referer': 'https://flippingpal.com/'
    }
    
    session = requests.Session()
    login_data = None
    
    for url in login_urls:
        try:
            print(f"Tentativo di login su: {url}")
            res = session.post(url, json={"email": email, "password": password}, headers=headers_base, timeout=20)
            if res.status_code == 200:
                login_data = res.json()
                print(f"LOGIN RIUSCITO su {url}!")
                break
            else:
                print(f"Fallito {url}: Stato {res.status_code}")
        except Exception as e:
            print(f"Errore tecnico su {url}: {e}")

    if not login_data or 'accessToken' not in login_data:
        print("IMPOSSIBILE EFFETTUARE IL LOGIN: Controlla email/password nei Secrets.")
        return

    token = "Bearer " + login_data.get('accessToken')
    user_id = login_data.get('user', {}).get('id')
    headers_auth = headers_base.copy()
    headers_auth['authorization'] = token
    
    market_url = "https://api.flippingpal.com/retail/market/ah-data-undercut/eu"
    realms = [3679,1325,3713,1104,3686,512,1302,3702,578,1406,1597,1417,580,581,1416,1393,1307,1127,1084,531,1618,1121,1403,1092,1378,3691,1315,1091,3692,1385,3703,509,1401,3657,1303,1587,1390,1596,1305,1080,3690,633,1082,1388,570,3681,1098,1621,1085,1624,1105,612,1316,3696,1408,1301,1309,1396,3682,1329,1099,1096,3666,1598,3391,3656,2073,1331,2074,604,1405,1402,3674,1384,1122,1400,510,1313,1097,1335,1379]

    try:
        print("Scarico i dati del mercato...")
        r = session.post(market_url, headers=headers_auth, json={"retailSellingRealms": realms, "retailBuyingRealms": realms, "userId": user_id}, timeout=600)
        data = r.json()

        html = "<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;background:#121212;color:white;padding:20px} .cat-box{border:1px solid #444;margin-bottom:20px;padding:15px;border-radius:8px} .buy{color:#4caf50} .sell{color:#f44336} table{width:100%} td{padding:5px}</style></head><body>"
        html += "<h1>Dashboard WoW - Ultimo Aggiornamento</h1>"

        categorie = ["Weapon", "Armor", "Container", "Consumable", "Glyph", "Trade Goods", "Recipe", "Gem", "Miscellaneous", "Quest", "Hollow"]
        for cat in categorie:
            items = [i for i in data if isinstance(i, dict) and i.get('category') == cat]
            if not items: continue
            
            srv_prices = {}
            for i in items:
                s = i.get('realmId'); p = i.get('price', 0)
                if s not in srv_prices: srv_prices[s] = []
                srv_prices[s].append(p)
            
            sorted_srv = sorted({s: sum(p)/len(p) for s, p in srv_prices.items()}.items(), key=lambda x: x[1])
            
            html += f"<div class='cat-box'><h2>{cat}</h2><table><tr>"
            html += "<td><b>Top Acquisto</b><br>"
            for s, p in sorted_srv[:10]: html += f"<span class='buy'>Server {s}</span>: {round(p/10000)}g<br>"
            html += "</td><td><b>Top Vendita</b><br>"
            for s, p in sorted_srv[-5:]: html += f"<span class='sell'>Server {s}</span>: {round(p/10000)}g<br>"
            html += "</td></tr></table></div>"

        html += "</body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("SUCCESSO: File index.html generato!")

    except Exception as e:
        print(f"Errore durante l'analisi dati: {e}")

if __name__ == "__main__":
    login_e_analizza()
