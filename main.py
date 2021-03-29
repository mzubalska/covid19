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

# VISUALIZATION

countries = ['Italy', 'Poland', 'Germany', 'Spain', 'Austria']

def confirmed_cases_plot():
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title('Covid-19 - total confirmed cases by country', color='white')

    for country in countries:
        confirmed[country][-90:].plot(label=country)

    plt.legend(loc='upper left')
    plt.show()

#confirmed_cases_plot()

def confirmed_cases_hist():
    for country in countries:
        ax = plt.subplot()
        ax.set_facecolor('black')
        ax.figure.set_facecolor('#121212')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set_title(f'Covid-19 - confirmed cases rate {country}', color='white')
        growth_rate[country][-60:].plot.bar()
        plt.show()

#confirmed_cases_hist()

def total_death_plot():
    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title('Covid-19 - total deaths by country', color='white')

    for country in countries:
        deaths[country][-90:].plot(label=country)

    plt.legend(loc='upper left')
    plt.show()

#total_death_plot()

def deaths_rate_hist():
    for country in countries:
        ax = plt.subplot()
        ax.set_facecolor('black')
        ax.figure.set_facecolor('#121212')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.set_title(f'Covid-19 - total deaths {country}', color='white')
        death_rate[country].plot.bar()
        plt.show()

#deaths_rate_hist()

simulated_growth_rate = 0.1

dates = pd.date_range(start='3/27/2021', periods=40, freq='D')
dates = pd.Series(dates)
dates = dates.dt.strftime('%m/%d/%Y')

simulated = confirmed.copy()
simulated = simulated.append(pd.DataFrame(index=dates))
#print(simulated)

def simulation_plot():
    for day in range(len(confirmed), len(confirmed)+40):
        simulated.iloc[day] = simulated.iloc[day - 1] * (1 + simulated_growth_rate)

    ax = plt.subplot()
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.set_title('Future simulation for Poland', color='white')
    simulated['Poland'].plot()
    plt.show()
#simulation_plot()


estimated_death_rate = 0.025

# infected * death_rate - deaths
# infected = deaths / death_rate
print(deaths['Italy'].tail()[4] / estimated_death_rate)
