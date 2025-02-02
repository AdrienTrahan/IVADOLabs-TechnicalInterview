import pandas as pd
from .wikiloader import WikiLoader 
import wikitextparser as wtp
import re
import os

COUNTRY_COLUMNS = ["COUNTRY_NAME", "COUNTRY_CODE"]

# Ideally, this is imported from a file and not hardcoded
EDGE_CASES = {
    "kingdom of the netherlands": "netherlands",
    "vatican city": "vatican",
    "taiwan, china": "taiwan"
}

class CountryLoader(WikiLoader):
    def __init__(self):
        super().__init__(
            pageName="ISO_3166-1_alpha-2",
            dataPath=os.path.join("data", "countries.csv"),
            languageCode="en"
        )
    
    def createDataFrame(self, rows):
        dataFrame = pd.DataFrame(rows, columns=COUNTRY_COLUMNS)
        dataFrame[COUNTRY_COLUMNS[0]] = dataFrame[COUNTRY_COLUMNS[0]].map(EDGE_CASES).fillna(dataFrame[COUNTRY_COLUMNS[0]])
        return dataFrame

    def formatRow(self, row):
        if (len(row) < 2): return None
        code = self.parseIsoCode(row[0])
        country = self.parseCountryName(row[1])
        if (code == None or country == None): return None
        return [country,code]
    
    def parseIsoCode(self, code):
        try:
            parsedName = wtp.parse(code);
            cellTitle = parsedName.wikilinks[0].title;
            if (not cellTitle.startswith("ISO 3166-2:")): return None;
            isoCode = parsedName.templates[0].arguments[0].value;
            if (len(isoCode) != 2): return None;
            isoCode = re.sub(r'[^a-zA-Z]', '', isoCode);
            if (len(isoCode) != 2): return None;
            return isoCode;
        except:
            return None
        
    def parseCountryName(self, name):
        try:
            parsedName = wtp.parse(name);
            return parsedName.wikilinks[0].title.lower();
        except:
            return None