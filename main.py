from dataloaders import loadMuseumVisitorData
from plotter import plotMuseumData

print("Loading data...")
museumVisitorData = loadMuseumVisitorData();
if (museumVisitorData is None): 
    print("Unable to load data");
    exit(1)

params = plotMuseumData(museumVisitorData)
if (params is not None): print(f"Intercept is {params[0]}, slope is {params[1]} with R2 = {params[2]}")

# Remove Tokyo from the data since its population is clearly outlier data
cleanedData = museumVisitorData[museumVisitorData["CITY_NAME"] != "tokyo"]
params = plotMuseumData(cleanedData, title = 'City Population vs Museum Visitor Count without Tokyo')
if (params is not None): 
    print("\nWithout Tokyo:")
    print(f"Intercept is {params[0]}, slope is {params[1]} with R2 = {params[2]}")