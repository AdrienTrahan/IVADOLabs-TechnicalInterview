
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors

def plotMuseumData(museumVisitorData, title='City Population vs Museum Visitor Count'):
    try:
        # Regression
        X = np.hstack((
            np.ones((len(museumVisitorData), 1)),
            museumVisitorData[['Population']].to_numpy()
        ))
        Y = museumVisitorData[['VISITOR_COUNT']].to_numpy()
        coefficients, *_ = np.linalg.lstsq(X, Y)
        Y_pred = X @ coefficients
        TSS = np.sum((Y - np.mean(Y)) ** 2)
        RSS = np.sum((Y - Y_pred) ** 2)
        R_squared = 1 - (RSS / TSS)

        # Plot
        scatter = plt.scatter(museumVisitorData['Population'], museumVisitorData['VISITOR_COUNT'], color='blue', label='Data Points')

        xRange = np.linspace(museumVisitorData['Population'].min(), museumVisitorData['Population'].max(), 100)
        predictedYRange = coefficients[0] + coefficients[1] * xRange
        plt.plot(xRange, predictedYRange, color='red')

        plt.xlabel('City Population')
        plt.ylabel('Visitor Count')
        plt.title(title)
        plt.legend()
        def millions_formatter(x, _):
            return f'{x / 1e6:.1f}M'

        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))
        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))
        
        cursor = mplcursors.cursor(scatter, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            x, y = sel.target[0], sel.target[1]
            
            distances = np.sqrt((museumVisitorData['Population'] - x) ** 2 + (museumVisitorData['VISITOR_COUNT'] - y) ** 2)
            index = distances.idxmin()
            
            name = museumVisitorData.loc[index, 'MUSEUM_NAME']
            country = museumVisitorData.loc[index, 'COUNTRY_NAME']
            population = museumVisitorData.loc[index, 'Population']
            visitor_count = museumVisitorData.loc[index, 'VISITOR_COUNT']
            
            sel.annotation.set_text(f"{name}\n{country}\nPopulation: {population}\nVisitors: {visitor_count}")

        plt.show()
        return (*coefficients, R_squared)
    except:
        return None
