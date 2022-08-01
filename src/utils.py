import datetime
import pandas as pd


def verify_number_elements(dataframe_gym_data: pd, number_elements: int) -> int:
    """
    Count number elements dataframe
    Args:
        :param  dataframe_gym_data: gym dataframe
        :param  number_elements: number elements to verify
    Returns:
        count_element: count elements dataframe
    """
    count_elements = len(dataframe_gym_data.index)
    if count_elements > number_elements:
        print(f"Task 2 : There are more than 50 000 rows in the dataset, "
              f"{count_elements} rows.\n")
    else:
        print(f"Task 2 : There are more not than 50 000 rows in the dataset, "
              f"{count_elements} rows.\n")
    return count_elements


def verify_range_records(dataframe: pd, start_date:str, end_date:str) -> int:
    """
    Verify if exist records between start_date and end_date (INCLUSIVE)
    Args:
        :param  dataframe: dataframe to verify
        :param  start_date: start date
        :param  end_date: end date
    Returns:
        count_results : number of records in the range dates
    """
    end_date = end_date[0:10]
    added_one_day_end_date = str(datetime.datetime.strptime(end_date, '%Y-%m-%d') +
                                 datetime.timedelta(days = 1))[0:10]
    df_results = dataframe[(dataframe.time > start_date) &
                           (dataframe.time < added_one_day_end_date)]
    count_results = len(df_results.index)
    if count_results > 0:
        print(f"Task 2 : There are records between {start_date} and {end_date} "
              f"(inclusive), {count_results} rows.\n")
    else:
        print(f"Task 2 : There are not records between {start_date} and {end_date} "
              f"(inclusive), {count_results} rows.\n")
    return count_results

def verify_positive_values(dataframe: pd, count_elements: int) -> int:
    """
    Verify if all values are positive
    Args:
        :param  dataframe: dataframe to verify
        :param  count_elements: total rows dataframe
    Returns:
        number_negatives_values: count number negative values in the dataframe
    """
    df_all_positives = dataframe[(dataframe['19'] > 0) & (dataframe['20'] > 0) &
                                 (dataframe['21'] > 0) & (dataframe['22'] > 0) &
                                 (dataframe['23'] > 0) & (dataframe['24'] > 0) &
                                 (dataframe['25'] > 0) & (dataframe['26'] > 0)]

    count_all_positives = len(df_all_positives.index)
    number_negatives_values = count_elements - count_all_positives
    if number_negatives_values > 0:
        print(f"Task 2 : Not all values in the dataframe are positives: "
              f"{number_negatives_values} rows has negative values.\n")
    else:
        print("Task 2 : All values in the dataframe are positives.\n")
    return number_negatives_values

def most_popular_device(df_hourly: pd) -> str:
    """
    Identify most popular device during the tracking period
    measured by number of minutes used
    Args:
        :param  df_hourly: hourly aggregated dataframe
    Returns:
        popular_device: most popular device id
    """
    series_sum_elements = df_hourly.sum(axis=0)[1:] # Filter first row, it is date
    list_sum = list(series_sum_elements.items())
    maximum_value = 0
    for device, sum_value in list_sum:
        if sum_value > maximum_value :
            maximum_value = sum_value
            popular_device = device
    print(f"Task 3 : The most popular device is {popular_device}, "
          f"used in total {maximum_value} minutes.\n")
    return popular_device


def is_hour_impacting_popularity(df_hourly: pd) -> None:
    """
    Verify if time of day (hour) impact overall popularity of the outdoor gym
    Args:
        :param  df_hourly: hourly aggregated dataframe
    Returns:
        Popularity of devices by hour
    """
    df_sum_device_hourly = df_hourly.\
        groupby([df_hourly['time'].str.slice(11, )]).sum()
    df_sum_hourly = df_sum_device_hourly.sum(axis=1)
    print("Task 3 : Definitely, time of day (hour) impact overall popularity of the outdoor gym, \n"
          "it is continuously increasing until 15 hours, then there is a reduction of device usage, \n"
          "in the below table (total device usage by hour), it is expressed this trend.\n")
    print(df_sum_hourly)

def popularity_gym_weekends_weekdays(df_hourly: pd) -> None:
    """
    Verify if the gym was more popular overall on weekends (Saturday and Sunday) than on weekdays
    Args:
        :param  df_hourly: hourly aggregated dataframe
    Returns:
        Verification usage weekends and weekdays
    """
    df_hourly['Weekday'] = df_hourly.apply(lambda x: weekday(x['time']), axis=1)
    df_weekends = df_hourly[(df_hourly.Weekday == 5) | (df_hourly.Weekday == 6)]
    df_sum_weekends = df_weekends.sum(axis=0)[1:9] # Filter only devices
    usage_weekends = df_sum_weekends.sum(axis=0)
    df_weekdays = df_hourly[(df_hourly.Weekday >= 0) | (df_hourly.Weekday < 5)]
    df_sum_weekdays = df_weekdays.sum(axis=0)[1:9] # Filter only devices
    usage_weekdays = df_sum_weekdays.sum(axis=0)
    if usage_weekends > usage_weekdays:
        print(f"Task 3 : Yes, the gym was more popular overall on weekends than on weekdays\n"
              f"usage weekends = {usage_weekends} minutes, usage weekdays = {usage_weekdays} minutes.\n")
    else:
        print(f"Task 3 : No, the gym was not more popular overall on weekends than on weekdays\n"
              f"usage weekends = {usage_weekends} minutes, usage weekdays = {usage_weekdays} minutes.\n")

def weekday(date_string: str) -> int:
    """
    Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    Args:
        :param  date_string: date in string format
    Returns:
        day of the week
    """
    return datetime.datetime.strptime(date_string[0:10], '%Y-%m-%d').weekday()
