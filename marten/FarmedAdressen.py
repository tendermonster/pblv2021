import pandas as pd

class FarmedAdressen():
    
    def __init__(self):
        self.df = pd.read_csv('./data/reports02022021.csv')
        self.df = self.df.drop(columns=['description', 'abuse_type_other'])
        self.df_addr = pd.read_csv('./data/addresses.csv')
        
    def get_reported_adressen(self):
        return self.df
    
    def get_wallet_adressen(self):
        return self.df_addr

