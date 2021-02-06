import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['all','january', 'february', 'march', 'april', 'may', 'june']
weekdays = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def choice(response, choices=('yes', 'no')):
    """Returns a valid response or choice from the raw user input
    """
    # each user input goes through function for validation
    while True:
        # we try to mitigate and clean possible responses e.g. random capitals or whitespaces
        choice = input(response).strip().lower()
        # terminate programs whenever user input is 'end'
        if choice == 'end':
            # exits loop and system
            raise SystemExit
        # allow user input when single answer without a comma
        elif ',' not in choice:
            if choice in choices:
                break
        # if input has more than one answer, separated by commas and assigns into a list
        elif ',' in choice:
            choice = [i.strip().lower() for i in choice.split(',')]
            if list(filter(lambda x: x in choices, choice)) == choice:
                break
        # all other responses would not be accepted
        response = ('\nSomething went wrong. Please check the formatting of your response and try again.\n')
    return choice


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze, or multiple cities
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! You can type \'end\' to exit the program at anytime.')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = choice('\nSelect one (or more) of the following cities: Chicago, New York City, or Washington. Please '
                    'separate by commas if more than one city.\n', CITY_DATA.keys())
        # get user input for month (january, february, ... , june)
        month = choice('\nFrom January to June, which month(s) would you like to filter data? Please separate '
                       'by commas if more than one month.\n>', months)
        # get user input for day of week (monday, tuesday, ... sunday)
        day = choice('\nWhich weekday(s) would you like to filter bikeshare data? Please use commas to list the names.\n>', weekdays)

        # ask to confirm of user input before calculation begins
        confirm = choice('\nPlease confirm your selected bikeshare data filter(s).\n\n City or Cities: {}\n Month(s): {}\n Weekday(s): {}\n\n [yes]\n [no]\n\n>'.format(city, month, day))

        if confirm == 'yes':
            break
        # while loop runs again if user does not confirm
        else:
            print('\nOk, no problem! Let\'s try again!')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month(s) and day(s) if applicable.

    Args:
        (str) city - name of the city to analyze OR (list) cities
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    print('\nPlease wait while the program loads the selected Bikeshare data.\n')
    start_time = time.time()

    # case when more than one city is selected
    if isinstance(city, list):
        # combine csv files of multiple cities
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # format columns of concatenated files, there is an extra column which would have stored different set of indices in the 'unnamed' column
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])

        # if there is an error, we do not want empty code
        except:
            pass
    else:
        #load data file into a dataframe for a single city
        df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and start hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Start_Hour'] = df['Start Time'].dt.hour



    # case when multiple months are selected
    if isinstance(month, list):
        # concatenate the chosen months
         df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month))], month))

    # apply month filter if applicable
    elif month != 'all':
        # only a single month is chosen
        # use the index of the months list to get the corresponding int
        month = months.index(month.lower())
        # filter by month to create the new dataframe
        df = df.loc[df['Month'] == month]

    # case when multiple weekdays are selected
    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Day_of_Week'] == (day.title())], day))
    # apply day filter if applicable
    elif day != 'all':
        # when a single day is selected
        df = df.loc[df['Day_of_Week'] == day.title()]


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most common month for travel is: ', months[popular_month].title())

    # display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print('The most common day for travel is: ', popular_day)

    # display the most common start hour
    popular_hour = df['Start_Hour'].mode()[0]
    print('The most common hour for travel is: {}h00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = str(df['Start Station'].mode()[0])
    print('The most commonly used Start Station is: ', popular_start_station)

    # display most commonly used end
    popular_end_station = str(df['End Station'].mode()[0])
    print('The most commonly used End Station is: ', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    popular_station_combo = str((df['Start Station'] + ' - ' + df['End Station']).mode()[0])
    print('The most frequent combination of Start Station and End Station is: ', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # convert seconds to different time intervals for easy user comprehension
    total_travel_time = (str(int(total_travel_time // 86400)) + ' day(s) ' +
                         str(int((total_travel_time % 86400) // 3600)) + ' hour(s) ' +
                         str(int(((total_travel_time % 86400) % 3600) // 60)) + ' minute(s) ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) + ' second(s)')
    print('The total travel time is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # convert to minutes and seconds
    mean_travel_time = (str(int(mean_travel_time // 60)) + ' minute(s) ' +
                       str(int(mean_travel_time % 60)) + ' second(s) ')
    print('The mean travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types as a string
    user_types = df['User Type'].value_counts().to_string()
    print('This is the distribution of users:')
    print(user_types)

    # Displays counts of gender
    try:
        gender_types = df['Gender'].value_counts().to_string()
        print('This is the breakdown of gender:')
        print(gender_types)
    # Cases where there does not exist a Gender column
    except KeyError:
        print('\nSorry, there is no gender data available for this city.\n')

    # Display earliest, most recent, and most common year of birth
    try:
        print('Customer birth year metrics:')
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print('The eldest customer was born in the year: ', earliest_birth_year)
        recent_birth_year = str(int(df['Birth Year'].max()))
        print('The youngest customer was born in the year: ', recent_birth_year)
        common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print('The most common year of birth among customers: ', common_birth_year)
    except:
        print('\nSorry, no data is available about birth year in this city.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Raw data is displayed upon request by user """
    # displays the heading of raw data
    print(df.head())
    # set row number
    row = 0
    while True:
        # prompt user to view additional raw data upon request
        view_raw_data = input('\nWould you like to view next five row of raw data? [yes] or [no]?\n')
        if view_raw_data.lower() != 'yes':
            return
        row += 5
        print(df.iloc[row:row + 5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            view_raw_data = input('\nWould you like to display first five rows of raw data? [yes] or [no]?\n')
            if view_raw_data.lower() != 'yes':
                break
            raw_data(df)
            break
        # ask user if program should restart
        restart = input('\nWould you like to restart this program? [yes] or [no]?\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
