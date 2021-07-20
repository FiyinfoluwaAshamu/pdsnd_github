#Import all packages needed
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
    print("Hello! Let's explore some US bikeshare data!")
    # User input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
      city = input("\n Which of this cities would you like to filter by? New York City, Chicago, or Washington?\n").lower()
      if city not in ("new york city", "chicago", "washington"):
        print ("Invalid entry, please try again.")
        continue
      else:
        break


    # User input for month (all, january, february, ... , june)
    while True:
      month = input("\n Would you like to filter by any of these months - January, February, March, April, May, June? type 'any' if you don't have a preference\n").lower()
      if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'any'):
        print ("Invalid entry, please try again.")
        continue

      else:
        break



    # User input for day of week (all, monday, tuesday, ... sunday)
    while True:
      day = input("\n Would you like to filter by any of these days - monday, tuesday, wednesday, thursday, friday, saturday,sunday? type 'all' if you don't have a preference\n").lower()
      if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",  "any"):
        print ("Invalid entry, please try again.")
        continue
      else:
        break


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
  #load data for city into a dataframe
  df = pd.read_csv(CITY_DATA[city])

  # convert the Start Time column to datetime
  df['Start Date'] = pd.to_datetime(df['Start Time'])
  # extract month and day from the Start Time column to create an hour column
  df['month'] = df['Start Date'].dt.month
  df['day'] = df['Start Date'].dt.day_name()


  #filter by month if applicable
  if month != 'all':
    # use the index of the months list to get the corresponding int
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months.index(month) + 1
    # filter by month to create the new dataframe
    df = df[df['month'] == month]

  # filter by day of week if applicable
  if day != 'all':
    # filter by day of week to create the new dataframe
    df = df[df['day'] == day.title()]


  return df


def time_stats(df):
  """Displays statistics on the most frequent times of travel."""

  print('\nCalculating The Most Frequent Times of Travel...\n')
  start_time = time.time()

  # to display the most common month
  common_month = df['month'].mode()[0]
  print('Most common month:', common_month)


  # Display the most common day of week
  common_day = df['day'].mode()[0]
  print('Most common day of the week:', common_day)


  #Display the most common start hour
  df['hour'] = df['Start Date'].dt.hour
  common_hour = df['hour'].mode()[0]
  print('Most common hour:', common_hour)


  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def station_stats(df):
  """Displays statistics on the most popular stations and trip."""
  print('\nCalculating The Most Popular Stations and Trip...\n')
  start_time = time.time()

  # Display most commonly used start station
  common_start_station = df['Start Station'].value_counts().idxmax()[0]
  print('Most commonly used start station:', common_start_station)


  # Display most commonly used end station
  common_end_station = df['End Station'].value_counts().idxmax()[0]
  print('Most commonly used end station:', common_end_station)


  # Display most frequent combination of start station and end station trip
  combination_of_station = df.groupby(['Start Station', 'End Station']).count()
  print('\nMost frequently used combination of start station and end station trip:', common_start_station, " & ", common_end_station)



  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def trip_duration_stats(df):
  """Displays statistics on the total and average trip duration."""

  print('\nCalculating Trip Duration...\n')
  start_time = time.time()

  # To display total travel time
  # There are 86400 seconds in a day. Therefore to get the total travel time, the sum of the trip duration is divided by 86400
  Total_Travel_Time = sum(df['Trip Duration'])
  print('Total travel time:', Total_Travel_Time/86400, " Days")


  # Display mean travel time
  #There are 60 seconds in a minute.
  Mean_Travel_Time = df['Trip Duration'].mean()
  print('Mean travel time:', Mean_Travel_Time/60, " Minutes")


  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def user_stats(df):
  """Displays statistics on bikeshare users."""

  print('\nCalculating User Stats...\n')
  start_time = time.time()

  # Display counts of user types by printing value counts for each user type
  user_types = df['User Type'].value_counts()
  print('Count of User Types:\n', user_types)


  #Display counts of gender
  try:
    gender_types = df['Gender'].value_counts()
    print('\nGender Types:\n', gender_types)

  except KeyError:
    print("\nGender Types:\nData not available for this month.")


  # The earliest, most recent, and most common year of birth
  try:
    earliest_year = df['Birth Year'].min()
    print('\nEarliest Year of Birth:', earliest_year)

  except KeyError:
    print("\nEarliest Year of Birth:\nData not available for this month.")

  try:
    most_recent_year = df['Birth Year'].max()
    print('\nMost Recent Year of Birth:', most_recent_year)

  except KeyError:
    print("\nMost Recent Year of Birth:\nData not available for this month.")

  try:
    most_common_year = df['Birth Year'].value_counts().idxmax()
    print('\nMost Common Year of Birth:', most_common_year)
  except KeyError:
    print("\nMost Common Year of Birth:\nData not available for this month.")


  print("\nThis took %s seconds." % (time.time() - start_time))
  print('-'*40)


def view_data(df):
  raw_data = 0
  while True:
    answer = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if answer not in ['yes', 'no', 'y', 'n']:
      answer = input("You wrote the wrong word. Please type Yes, No, N, or Y.").lower()
    elif answer == 'yes':
      raw_data += 5
      print(df.iloc[raw_data : raw_data + 5])

    again = input("Do you want to see more? Yes or No?")
    if again.lower() == 'no':
      break
    elif answer == 'no':
      return


def main():
  while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)

    view_data(df)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
      break


if __name__ == "__main__":
	main()
