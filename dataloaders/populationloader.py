from .dataloader import DataLoader
import os
import pandas as pd
from .utils import formatCity
import kagglehub
import shutil

POPULATION_COLUMNS = ["Country", "City", "Population"]
# Ideally, this is imported from a file and not hardcoded
EDGE_CASES = {
    "peking": "beijing",
}

class PopulationLoader(DataLoader):
    def __init__(self):
        super().__init__(
            dataPath=os.path.join("data", "worldcitiespop.csv")
        )
        
    def get(self):
        try:
            self.fetchData();
            dataFrame = self.load(columns=POPULATION_COLUMNS).dropna();
            
            dataFrame[POPULATION_COLUMNS[0]] = dataFrame[POPULATION_COLUMNS[0]].str.upper()
            dataFrame[POPULATION_COLUMNS[1]] = dataFrame[POPULATION_COLUMNS[1]].apply(formatCity)
            dataFrame = dataFrame.explode(POPULATION_COLUMNS[1])
            
            dataFrame[POPULATION_COLUMNS[1]] = dataFrame[POPULATION_COLUMNS[1]].map(EDGE_CASES).fillna(dataFrame[POPULATION_COLUMNS[1]])
            dataFrame[POPULATION_COLUMNS[2]] = pd.to_numeric(dataFrame[POPULATION_COLUMNS[2]], errors='coerce').dropna()
            
            return dataFrame
        except:
            return None
        
    def fetchData(self):
        if not os.path.exists(self.dataPath):
            path = kagglehub.dataset_download("max-mind/world-cities-database")
            filePath = os.path.join(path, "worldcitiespop.csv")
            os.makedirs(os.path.dirname(self.dataPath), exist_ok=True)
            shutil.copy(filePath, self.dataPath)