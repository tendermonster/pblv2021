import os
import json
import requests

class Adressen():
    
    def __init__(self):
        if not os.path.isdir('adressen'):
            os.mkdir('adressen')
        try:
            self.local_addresses = [addr for addr in os.walk('adressen')]
            self.local_addresses = [addr[:-5] for addr in self.local_addresses[0][2]]
        except: 
            self.local_addresses = []
    
    
    def getAddress(self, address):
        if address in self.local_addresses:
            with open(f'adressen/{address}.json', 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f"Adresse {address} nicht vorhanden!")
            
    def downloadAddress(self, address):
        url = f'https://blockchain.info/rawaddr/{address}'
        r = requests.get(url)
        if r.status_code != 200:
            raise ValueError(f'Request nicht erfolgreich. Statuscode: {r.status_code}')
        with open(f'adressen/{address}.json', 'w') as f:
            json.dump(r.json(), f)
        self.local_addresses.append(address)
        return r.json()
                           