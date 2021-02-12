import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime


class TransactionsMempool():
    """
    Berechnet die Anzahl der Transaktionen im Mempool. Die Daten dafür liegen im 5-Minuten Rythmus vor.
    """
    
    def __init__(self):
        self.df = pd.read_csv('./marten/amount_transactions.csv')
        self.df_blocks = pd.read_csv('./marten/tx_per_block.csv')
        self.timestamps = self.convert_to_timestamps()
        
    def convert_to_timestamps(self):
        timestamps = []

        for date in self.df.date:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            hours = int(date[11:13])
            minutes = int(date[14:16])

            t = int(datetime.datetime(year,month,day,hours,minutes).timestamp())
            timestamps.append(t)
            
        return timestamps
    
    def get_avg(self):
        return np.average(self.df['amount_tx'])
    
    def get_median(self):
        return self.df['amount_tx'].median()
         
        
    def save_graph(self, filename='txs_in_mempool.png'):
        plt.plot([self.df_blocks.timestamp.iloc[0], self.df_blocks.timestamp.iloc[0]],
                 [self.df['amount_tx'].min(), self.df['amount_tx'].max()], '--', color='grey', label='Block')

        for t in self.df_blocks.timestamp[1:]:
            plt.plot([t, t], [self.df['amount_tx'].min(), self.df['amount_tx'].max()], '--', color='grey')

            
        _ = plt.plot([min(self.timestamps), max(self.timestamps)] ,[self.df['amount_tx'].quantile(), self.df['amount_tx'].quantile()], color='firebrick')
        
        _ = plt.plot([min(self.timestamps), max(self.timestamps)] ,[self.df['amount_tx'].quantile(0.25), self.df['amount_tx'].quantile(0.25)], '--', color='firebrick')
        
        _ = plt.plot([min(self.timestamps), max(self.timestamps)] ,[self.df['amount_tx'].quantile(0.75), self.df['amount_tx'].quantile(0.75)], '--',color='firebrick')
        
        _ = plt.plot(self.timestamps, self.df['amount_tx'], label='Transaktionen')
        _ = plt.title('Transaktionen im Mempool')
        _ = plt.legend(loc='upper left')
        _ = plt.xticks([])
        _ = plt.xlabel('Zeitstrahl')
        _ = plt.ylabel('Anzahl Transaktionen')
        _ = plt.savefig(filename)
        

class TransactionsBlock():
    
    def __init__(self):
        self.df_blocks = pd.read_csv('./marten/tx_per_block.csv')
        
    def get_avg(self):
        return np.average(self.df_blocks['tx_count'])
    
    def get_median(self):
        return self.df_blocks['tx_count'].quantile()
    
    def save_graph(self, filename='txs_in_block.png'):
        x_vals = [i for i in range(self.df_blocks['tx_count'].shape[0])]
        _ = plt.plot([min(x_vals), max(x_vals)] ,[self.df_blocks['tx_count'].quantile(), self.df_blocks['tx_count'].quantile()], color='firebrick')
        _ = plt.plot([min(x_vals), max(x_vals)] ,[self.df_blocks['tx_count'].quantile(0.25), self.df_blocks['tx_count'].quantile(0.25)], '--', color='firebrick')
        _ = plt.plot([min(x_vals), max(x_vals)] ,[self.df_blocks['tx_count'].quantile(0.75), self.df_blocks['tx_count'].quantile(0.75)], '--',color='firebrick')
        _ = plt.plot(x_vals, self.df_blocks['tx_count'])
        _ = plt.title('Anzahl Transaktionen in einem Block')
        _ = plt.xticks([])
        _ = plt.savefig(filename)
        
   
class Blockdifference():
    """
    Berechnet die Zeit zwischen der Erstellung von zwei Blöcken.
    """
    def __init__(self):
        self.df_blocks = pd.read_csv('./marten/tx_per_block.csv')
        self.differences = self.__get_differences__()
        
    def __get_differences__(self):
        dates = [datetime.datetime.fromtimestamp(t) for t in self.df_blocks.timestamp]
        differences = []
        for i in range(1,len(dates)):
            differences.append((dates[i] - dates[i-1]).seconds)
        return differences
        
    def get_avg(self):
        return np.average(self.differences)
    
    def get_median(self):
        return np.median(self.differences)   
        
    
    def tx_pro_block(self):
        return f"Alle {int(round(np.average(self.differences) / 60, 0))} Minuten werden {int(np.average(self.df_blocks['tx_count']))} Transaktionen aus dem Mempool entfernt."
    
    
    def save_graph(self, filename='block_difference.png', showmedian=False):
        if showmedian:
            _ = plt.plot([0, len(self.differences)], [np.median(self.differences), np.median(self.differences)], '--', color='firebrick')
        _ = plt.plot([0, len(self.differences)], [np.average(self.differences), np.average(self.differences) ], '--', color='green')
        _ = plt.plot(self.differences)
        _ = plt.title('Zeitlicher Abstand zwischen zwei Blöcken')
        _ = plt.ylabel('Zeit in s')
        _ = plt.xlabel('Blöcke')
        _ = plt.xticks([])
        _ = plt.savefig(filename)

        
        
class NewTransactions():
    
    def __init__(self):
        self.df = pd.read_csv('./marten/amount_transactions.csv')
        self.df_blocks = pd.read_csv('./marten/tx_per_block.csv')
        self.__calc_timestamps__()
        self.new_txs = self.__get_new_txs__()

        
    def __calc_timestamps__(self):
        timestamps = []

        for date in self.df.date:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            hours = int(date[11:13])
            minutes = int(date[14:16])

            t = int(datetime.datetime(year,month,day,hours,minutes).timestamp())
            timestamps.append(t)

        self.df['timestamps'] = timestamps
    
    def __get_new_txs__(self):
        new_txs = []

        for i in range(1, len(self.df)):
            start = self.df.iloc[i-1]
            end = self.df.iloc[i]
            diff = (datetime.datetime.fromtimestamp(end.timestamps) - 
                    datetime.datetime.fromtimestamp(start.timestamps)).seconds / 60
            if diff >= 4.0 and diff <= 6.0:
                block_txs =  self.df_blocks[(self.df_blocks.timestamp >= start.timestamps) & 
                                   (self.df_blocks.timestamp <= end.timestamps)].tx_count.sum()

                new_txs.append(end.amount_tx + block_txs - start.amount_tx)
        return [i for i in new_txs if i > 0]
    
    def get_avg(self):
        """
        Durchschnittliche Anzahl neuer Transaktionen in 5 Minuten.
        """
        return np.mean(self.new_txs)
    
    def get_median(self):
        """
        Median von neuen Transaktionen im 5 Minuten Rythmus.
        """
        return np.quantile(self.new_txs, 0.5)    
    
    def get_10_cmp(self):
        b = Blockdifference()
        #pred_10 = self.df_blocks['tx_count'].mean() / np.quantile(b.differences, 0.5) * 600
        pred_10 = self.df_blocks['tx_count'].mean() / np.average(b.differences) * 600
        return f"Alle zehn Minuten werden {int(pred_10)} Transaktionen in Blöcken bestätigt, während {int(np.median(self.new_txs)*2)} neue Transaktionen erstehen"
    
    
    def save_graph(self, filename='5_minute_transactions'):
        x_vals = [i for i in range(len(self.new_txs))]
        _ = plt.plot([0, len(x_vals)], [np.quantile(self.new_txs, 0.5), np.quantile(self.new_txs, 0.5)], '--', color='firebrick')
        _ = plt.plot([0, len(x_vals)], [np.mean(self.new_txs), np.mean(self.new_txs)], '--', color='deeppink')
        _ = plt.plot(x_vals, self.new_txs)
        _ = plt.xticks([])
        _ = plt.title("Neue Transaktionen pro 5 Minuten")
        _ = plt.savefig('5_min_transactions.png')
    
    
