import pandas as pd
import os
class DataLoader:

    def __init__(self, dataPath):
        self.dataPath = dataPath;
    
    def get(self) -> pd.DataFrame: 
        pass

    def save(self, df):
        # make folders in case they don't exist
        folder_path = os.path.dirname(self.dataPath)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        df.to_csv(self.dataPath, sep=',', index=False)

    def load(self, columns=None, types=None):
        folder_path = os.path.dirname(self.dataPath)
        if os.path.exists(folder_path):
            return pd.read_csv(self.dataPath, sep=',', usecols=columns, dtype=types)
        return None
