from abc import abstractmethod
import pandas as pd
import wikitextparser as wtp
import pywikibot as pwb
from .dataloader import DataLoader
from.errors import NetworkException, EmptyTableException

class WikiLoader(DataLoader):
    def __init__(self, pageName, dataPath, languageCode="en"):
        super().__init__(dataPath)
        self.pageName = pageName
        self.languageCode = languageCode;

    def get(self) -> pd.DataFrame: 
        dataFrame = self.scrapeRemoteData()
        if (dataFrame is not None):
            self.save(dataFrame);
            return dataFrame;
        else:
            return self.load();
    
    def scrapeRemoteData(self):
        try:
            rows = [];
            for table in self.fetchTables():
                tableContent = table.data();

                # Skip tables that have only a single row or less.
                # (row count includes the headers)
                if (len(tableContent) <= 1): continue;

                for row in tableContent[1:]:
                    try:
                        formattedRow = self.formatRow(row);
                        if (formattedRow is not None): rows.append(formattedRow);
                    except:
                        pass

            if (len(rows) == 0): raise EmptyTableException

            return self.createDataFrame(rows)
        except:
            return None
    
    def fetchTables(self):
        try:
            site = pwb.Site(self.languageCode, "wikipedia");
            page = pwb.Page(site, self.pageName);
            pageContent = page.get();
            parsed = wtp.parse(pageContent);
            for table in parsed.tables:
                if (callable(getattr(table, "data", None))): yield table
        except:
            raise NetworkException
        
    @abstractmethod
    def createDataFrame(self, rows):
        pass

    @abstractmethod
    def formatRow(self, row):
        pass
        

