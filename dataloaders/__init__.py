from .museumloader import MuseumLoader
from .countryloader import CountryLoader
from .populationloader import PopulationLoader
import pandas as pd

def loadMuseumVisitorData():
    museumsLoader = MuseumLoader()
    countriesLoader = CountryLoader()
    populationLoader = PopulationLoader()

    museumsDf = museumsLoader.get()
    countriesDf = countriesLoader.get()
    populationDf = populationLoader.get()

    if (museumsDf is None or
        countriesDf is None or
        populationDf is None): return None

    museumCountries = pd.merge(museumsDf, countriesDf, left_on='COUNTRY_NAME', right_on='COUNTRY_NAME', how='left')
    museumVisitorsDf = pd.merge(museumCountries, populationDf, left_on=['COUNTRY_CODE', 'CITY_NAME'], right_on=['Country', 'City'], how='inner')
    museumVisitorsDf = museumVisitorsDf.groupby(['MUSEUM_NAME', 'VISITOR_COUNT', 'COUNTRY_NAME', 'COUNTRY_CODE'], as_index=False).agg({
        'CITY_NAME': lambda x: list(x),
        'Population': 'first'
    })
    museumVisitorsDf['CITY_NAME'] = museumVisitorsDf['CITY_NAME'].apply(", ".join)
    museumVisitorsDf = museumVisitorsDf[['MUSEUM_NAME','VISITOR_COUNT', 'COUNTRY_NAME', 'COUNTRY_CODE', 'CITY_NAME', 'Population']]
    return museumVisitorsDf
