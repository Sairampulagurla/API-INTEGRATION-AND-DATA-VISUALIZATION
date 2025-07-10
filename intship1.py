# Let's gather our tools first
import requests  # For talking to the internet and getting data
import matplotlib.pyplot as plt  # Our trusty graphing companion
from datetime import datetime  # To handle dates like a pro
import matplotlib.dates as mdates  # For making dates look pretty on graphs

def fetch_covid_data(country='USA'):
    """
    Gets COVID-19 data for the specified country.

    Parameters:
        country: The country to get data for (default is USA)

    Returns:
        A tuple with three things:
        1. List of dates
        2. List of new cases each day
        3. List of new deaths each day

    Possible Errors:
        - If the data doesn't look right
        - If there's a problem connecting to the internet
    """
    # Building our request to the data provider
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=all"
    
    # Let's politely ask for the data
    print(f"Fetching COVID data for {country}... please wait...")
    response = requests.get(url)
    data = response.json()  # Turning the response into something we can work with

    # Making sure we got good data back
    if 'timeline' not in data:
        raise ValueError(f"Oops! We didn't get the expected data for {country}")

    # Unpacking the numbers we care about
    cases = data['timeline']['cases']  # All the cases over time
    deaths = data['timeline']['deaths']  # All the deaths over time

    # Sorting dates because sometimes life comes at us out of order
    dates = sorted(cases.keys(), key=lambda d: datetime.strptime(d, "%m/%d/%y"))

    # Calculating daily changes (new cases/deaths each day)
    daily_new_cases = []
    daily_new_deaths = []
    yesterday_cases = 0  # Starting our counters
    yesterday_deaths = 0
    
    for date in dates:
        today_cases = cases[date]
        today_deaths = deaths[date]

        # How many new since yesterday?
        new_cases = today_cases - yesterday_cases
        new_deaths = today_deaths - yesterday_deaths

        # Remember today's numbers for tomorrow's calculation
        yesterday_cases = today_cases
        yesterday_deaths = today_deaths

        # Sometimes data gets corrected - we'll ignore negative numbers
        daily_new_cases.append(new_cases if new_cases >= 0 else 0)
        daily_new_deaths.append(new_deaths if new_deaths >= 0 else 0)

    # Making dates into proper datetime objects for our graphs
    dates_dt = [datetime.strptime(d, "%m/%d/%y") for d in dates]

    return dates_dt, daily_new_cases, daily_new_deaths

def plot_dashboard(dates, daily_cases, daily_deaths, country='USA'):
    """
    we will create three panels showing:
    1. The daily rollercoaster of new cases
    2. The sobering daily death counts
    3. The big picture with cumulative totals
    """
    plt.style.use('ggplot')
    
    # making a three graphs display.
    fig, axs = plt.subplots(3, 1, figsize=(15, 18))
    
    # adjusting the graphs.
    plt.subplots_adjust(top=0.92, hspace=0.5)

    # Setting up how we'll display dates on our graphs
    date_locator = mdates.AutoDateLocator()  #  date spacing
    date_formatter = mdates.ConciseDateFormatter(date_locator)  # Clear date labels

    # --- First Graph: Daily Cases ---
    axs[0].plot(dates, daily_cases, color='crimson', label='Daily New Cases')
    axs[0].set_title(
        f'Daily COVID-19 Cases in {country}', 
        fontsize=14, 
        fontweight='bold', 
        pad=20  # Extra space so nothing gets cramped
    )
    axs[0].set_ylabel('Number of Cases')
    axs[0].xaxis.set_major_locator(date_locator)
    axs[0].xaxis.set_major_formatter(date_formatter)
    axs[0].legend()

    # --- Second Graph: Daily Deaths ---
    axs[1].plot(dates, daily_deaths, color='black', label='Daily New Deaths')
    axs[1].set_title(
        f'Daily COVID-19 Deaths in {country}', 
        fontsize=14, 
        fontweight='bold', 
        pad=20
    )
    axs[1].set_ylabel('Number of Deaths')
    axs[1].xaxis.set_major_locator(date_locator)
    axs[1].xaxis.set_major_formatter(date_formatter)
    axs[1].legend()

    # --- Third Graph: The Big Picture ---
    # Let's calculate the running totals
    total_cases = 0
    total_deaths = 0
    all_time_cases = []
    all_time_deaths = []
    
    for today_cases, today_deaths in zip(daily_cases, daily_deaths):
        total_cases += today_cases
        total_deaths += today_deaths
        all_time_cases.append(total_cases)
        all_time_deaths.append(total_deaths)

    # Plotting both totals together for comparison
    axs[2].plot(dates, all_time_cases, color='blue', label='Total Cases')
    axs[2].plot(dates, all_time_deaths, color='red', label='Total Deaths')
    axs[2].set_title(
        f'Total COVID-19 Impact in {country}', 
        fontsize=14, 
        fontweight='bold', 
        pad=20
    )
    axs[2].set_ylabel('Cumulative Count')
    axs[2].xaxis.set_major_locator(date_locator)
    axs[2].xaxis.set_major_formatter(date_formatter)
    axs[2].legend()

    # Some finishings so that our graphs look good.
    for graph in axs:
        graph.set_xlabel('Date')
        graph.grid(True, linestyle='--', alpha=0.5)  # Light grid lines for reference

    # The big title that ties everything together
    plt.suptitle(
        f'COVID-19 in {country}: The Story in Data', 
        fontsize=20, 
        fontweight='bold', 
        y=0.98  # adujusting positions.
    )
    plt.show()

def main():
    """
    Our main function - the conductor of this data orchestra!
    """
    print("Welcome to the COVID-19 Data Explorer!")
    print("Let's visualize how the pandemic unfolded in different countries.")
    
    # enter country name that you nedd to analyise.
    country = input("Which country are you interested in? (e.g., USA, Brazil, India): ").strip() or 'USA'

    try:
        # Let get the data and make it visual!
        print("Working on it... crunching numbers... drawing graphs...")
        dates, daily_cases, daily_deaths = fetch_covid_data(country)
        plot_dashboard(dates, daily_cases, daily_deaths, country)
    except Exception as e:
        print(f"Uh oh! We hit a snag: {e}")
        print("Maybe try a different country or check your internet connection?")

if __name__ == "__main__":
    main()