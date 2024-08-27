import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
     # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city name. Please enter either Chicago, New York City, or Washington.")
    
    # Get user input for month (all, january, february, ..., june)
    while True:
        month = input("Which month? January, February, March, April, May, June, or 'all' to apply no month filter: ").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Invalid month. Please enter a valid month from January to June, or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Please enter a day of the week (e.g., Monday, Tuesday) or 'all' to apply no day filter: ").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Invalid day. Please enter a valid day of the week or 'all'.")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    # Display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"Most Common Day of Week: {common_day_of_week}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_start_hour}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

     # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Start-End Combination'].mode()[0]
    print(f"Most Common Trip: {common_trip}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"Counts of User Types:\n{user_types}")

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nCounts of Gender:\n{gender_counts}")
    else:
        print("\nGender data not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest Year of Birth: {earliest_year}")
        print(f"Most Recent Year of Birth: {most_recent_year}")
        print(f"Most Common Year of Birth: {most_common_year}")
    else:
        print("\nBirth Year data not available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
    """
    Displays 5 rows of individual trip data at a time, based on user input.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    
    while view_data == 'yes' and start_loc < len(df):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no\n").lower()

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
