import os
import requests

def scarica_dati_final():
    token = os.getenv('FP_TOKEN')
    # L'indirizzo esatto confermato dai tuoi screenshot
    url = "https://api.flippingpal.com/retail/market/ah-data-undercut/eu"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }
    
    realms = [3679,1325,3713,1104,3686,512,1302,3702,578,1406,1597,1417,580,581,1416,1393,1307,1127,1084,531,1618,1121,1403,1092,1378,3691,1315,1091,3692,1385,3703,509,1401,3657,1303,1587,1390,1596,1305,1080,3690,633,1082,1388,570,3681,1098,1621,1085,1624,1105,612,1316,3696,1408,1301,1309,1396,3682,1329,1099,1096,3666,1598,3391,3656,2073,1331,2074,604,1405,1402,3674,1384,1122,1400,510,1313,1097,1335,1379]

    try:
        print("Avvio richiesta dati al server...")
        res = requests.post(url, headers=headers, json={"retailSellingRealms": realms, "retailBuyingRealms": realms})
        
        if res.status_code == 200:
            data = res.json()
            print(f"SUCCESSO! Ricevuti {len(data)} oggetti.")
            
            # Creazione HTML Dashboard
            html = "<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;background:#121212;color:white;padding:20px} .card{background:#1e1e1e;padding:15px;margin-bottom:10px;border-radius:5px;border-left:5px solid #4caf50} .gold{color:#ffd700}</style></head><body>"
            html += "<h1>Dashboard WoW - Dati Live</h1>"
            
            # Mostriamo i risultati più interessanti
            for item in data[:100]:
                nome = item.get('name', 'Oggetto Ignoto')
                prezzo = round(item.get('price', 0) / 10000)
                reame = item.get('realmId', '?')
                html += f"<div class='card'><b>{nome}</b>: <span class='gold'>{prezzo}g</span> (Server: {reame})</div>"
            
            html += "</body></html>"
            
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("File index.html aggiornato con successo.")
        else:
            print(f"Errore {res.status_code}: {res.text[:100]}")
            
    except Exception as e:
        print(f"Errore tecnico: {e}")

if __name__ == "__main__":
    scarica_dati_final()
