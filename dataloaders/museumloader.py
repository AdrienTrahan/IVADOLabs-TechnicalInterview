import pandas as pd
from .wikiloader import WikiLoader 
import wikitextparser as wtp
import re
from numerizer import numerize
from unidecode import unidecode
import os
from .utils import formatCity

MUSEUM_COLUMNS = ["MUSEUM_NAME", "VISITOR_COUNT", "COUNTRY_NAME", "CITY_NAME"]

class MuseumLoader(WikiLoader):
    def __init__(self):
        super().__init__(
            pageName="List_of_most-visited_museums",
            dataPath=os.path.join("data", "museums.csv"),
            languageCode="en"
        )
    
    def createDataFrame(self, rows):
        return pd.DataFrame(rows, columns=MUSEUM_COLUMNS).explode(MUSEUM_COLUMNS[3])

    def formatRow(self, row):
        if (len(row) < 4): return None
        museum = self.parseMuseumName(row[0])
        count = self.parseVisitorCount(row[1])
        city = self.parseCityName(row[2])
        country = self.parseCountryName(row[3])
        
        if (
            museum is None or
            count is None or
            country is None or
            city is None
        ): return None

        return [museum, count, country, city];

    def parseMuseumName(self, name):
        try:
            parsedContent = wtp.parse(name);
            return parsedContent.plain_text()
        except:
            return None
    
    def parseVisitorCount(self, count):
        try:
            parsedCount = wtp.parse(count);

            for tag in parsedCount.get_tags():
                if tag.name == 'ref': parsedCount.string = parsedCount.string.replace(str(tag), '')
            
            textCount = parsedCount.plain_text();
            # Remove text within parenthesis
            textCount = re.sub(r'\([^)]*\)', '', textCount);
            # Remove non alphanumeric characters and excluding .
            textCount = re.sub(r'[^(\w.)]', '', textCount);
            # Handles human words conversion
            textCount = numerize(textCount);
            textCount = re.sub(r'[,]', '', textCount);
            # This converts the string to integer
            # It also verifies for decimal numbers: 
            # It raises an error if the number is a decimal
            visitorCount = int(textCount);
            return visitorCount;
        except:
            return None;
    
    def parseCountryName(self, name):
        try:
            parsedName = wtp.parse(name);
            return parsedName.templates[0].arguments[0].value.lower();
        except:
            return None
    
    
    def parseCityName(self, name):
        try:
            parsedName = wtp.parse(name);
            cityName = parsedName.plain_text()
            return formatCity(cityName);
        except:
            return None