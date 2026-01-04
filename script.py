import os
import requests

def login_e_analizza():
    email = os.getenv('FP_EMAIL')
    password = os.getenv('FP_PASSWORD')
    
    # Intestazioni per sembrare un browser vero
    headers_base = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Origin': 'https://flippingpal.com',
        'Referer': 'https://flippingpal.com/'
    }
    
    login_url = "https://api.flippingpal.com/auth/login"
    
    try:
        print(f"Tentativo di login per: {email}")
        payload = {"email": email, "password": password}
        
        # Effettua la richiesta di login
        response = requests.post(login_url, json=payload, headers=headers_base)
        
        # Controlla se la risposta è valida
        if response.status_code != 200:
            print(f"Errore del server: Stato {response.status_code}")
            print(f"Risposta grezza: {response.text[:100]}")
            return

        login_data = response.json()
        # ... resto dello script ...
        print("Login riuscito!")
        
    except Exception as e:
        print(f"Errore durante l'operazione: {e}")

if __name__ == "__main__":
    login_e_analizza()
