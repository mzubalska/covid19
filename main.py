import pandas as pd
import matplotlib.pyplot as plt

confirmed = pd.read_csv('covid19_confirmed_global.csv')
deaths = pd.read_csv('covid19_deaths_global.csv')
recovered = pd.read_csv('covid19_recovered_global.csv')

confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)

confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T

# ile przyapdkow dziennie
new_cases = confirmed.copy()

for day in range(1, len(confirmed)):
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day - 1]
#print(new_cases.tail(10))

# przyrost procentowy
growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    growth_rate.iloc[day] = (new_cases.iloc[day] / confirmed.iloc[day - 1]) * 100
#print(growth_rate.tail(10))

# przypadki aktywne
active_cases = confirmed.copy()

for day in range(0, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - deaths.iloc[day] - recovered.iloc[day]

# procentowy przyrost aktywnych przypadkow
overall_growth_rate = confirmed.copy()

for day in range(1, len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day - 1]) / active_cases.iloc[day - 1]) * 100
#print(overall_growth_rate.tail(10))

death_rate = confirmed.copy()

for day in range(0, len(confirmed)):
    death_rate.iloc[day] = (deaths.iloc[day] / confirmed.iloc[day]) * 100

hospialization_rate_estimate = 0.05 # liczba osob ktore beda potrzebowac hospitalizacji
hospialization_needed = confirmed.copy()

for day in range(0, len(confirmed)):
    hospialization_needed.iloc[day] = active_cases.iloc[day] * hospialization_rate_estimate

# visualization

countries = ['Italy', 'Poland', 'Germany', 'Spain', 'Austria']

for country in countries:
    confirmed[country].plot(label=country)
plt.legend(loc='upper left')
plt.show()
