import pandas as pd
import requests
from graphviz import Digraph
from Adressen import Adressen
import json
import matplotlib.pyplot as plt
from time import sleep
from subprocess import check_call

class Cashflow():
    
    def __init__(self, address):
        self.address = address
        self.df = pd.read_csv('./data/reports02022021.csv')
        self.df = self.df.drop(columns=['description', 'abuse_type_other'])
        self.df_addr = pd.read_csv('./data/addresses.csv')
        
        self.local_addresses = Adressen()
        self.other_addresses = []
        self.receivers = {}
        self.cashflow = {}
        self.next_items = []
        self.cnt = 1
        
        
    def __repr__(self):
        return self.address
        
        
    def getAddress(self, address):
        try:
            return self.local_addresses.getAddress(address)['txs']
        except:
            sleep(30)
            if self.cnt < 3:
                return self.local_addresses.downloadAddress(address)['txs']
            else:
                raise ValueError("Too many requests")
            self.cnt += 1
    
    
    def receiver_is_wallet(self):
        flat_receivers = [item for sublist in self.receivers.values() for item in sublist]
        return any([a in self.df_addr.address.values for a in flat_receivers])

    
    def save_graph(self, filename=None):
        if filename is None:
            filename = 'cashflow.png'
        graph = self.plot()
        graph.save('cashflow.dot')
        check_call(['dot','-Tpng','cashflow.dot','-o', filename])
    
    
    def plot(self, color='red', dot_p=None):
        if dot_p is None:
            dot = Digraph()
        else:
            dot = dot_p
        dot.node(self.address, self.address[:3] + "..." + self.address[-3:], color=color)
        
        keys = [key for key in self.cashflow.keys()]
        if len(keys) > 3:
            keys = [keys[0], len(keys)-2, keys[-1]]
        
        self.__create_graph__(dot, keys)
        
        for cash in self.next_items:
            cash.plot(None, dot)            
        return dot
    
    
    def __create_graph__(self, dot, keys):
        for key in keys:
            if type(key) is int:
                name = self.address + str(key) 
                dot.node(name, "+ " + str(key)) 
                dot.edge(self.address, name)
            else:
                val = round(sum(self.cashflow[key]), 3)
                dot.node(key, key[:3] + "..." + key[-3:]) 
                dot.edge(self.address, key, str(val))
        
    
    def __cmp__(self, other):
        return self.address.__cmp__(other.address)
        
        
    def analyse(self, steps):
        return self.__analyse_cashflow__(0, steps)
        
    
    def __analyse_cashflow__(self, step, last_step):
        if step == last_step:
            return self.cashflow
                
        transactions = self.getAddress(self.address)
        
        for tx in range(len(transactions)):
            input_addrs = []
            for addr in transactions[tx]['inputs']:
                try:
                    input_addrs.append(addr['prev_out']['addr'])
                except:
                    continue
            if self.address in input_addrs:
                self.other_addresses.extend(input_addrs)
                self.other_addresses.remove(self.address)
            
                tx_hash = transactions[tx]['hash']
                self.receivers[tx_hash] = []
                
                for out in range(len(transactions[tx]['out'])):
                    try:
                        a = transactions[tx]['out'][out]['addr']
                        val = round(transactions[tx]['out'][out]['value'] / 100_000_000, 3)
                    except:
                        print(f'Fehler bei {tx} {out}')
                        continue
                    
                    if a in self.cashflow:
                        self.cashflow[a].append(val)
                    else:
                        self.cashflow[a] = [val]
                    
                    self.receivers[tx_hash].append(a)
                    
        keys = [item for item in self.cashflow.keys()]
        if len(keys) > 3:
            keys = [keys[0], keys[-1]]
            
        for i in keys:
            
            n = Cashflow(i)
            n.__analyse_cashflow__(step+1, last_step)
            self.next_items.append(n)
            
            
        return self.cashflow
        