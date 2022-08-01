"""
Analyze outdoor gym data (Hietaniemi dataset)
"""
import os
import logging
from joblib import dump, load
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

class OutdoorGymAnalysis:
    """
    Class for analyze outdoor gym data
    """

    def __init__(self):
        self.model = load("./models/model.pkl")

    def read_csv_data(self, file_path):
        """
        Read data from csv files
        Args:
            :param  file_path: csv file path
        Returns:
            response: data in pandas dataframe
        """
        try:
            dataframe = pd.read_csv(file_path)
            return dataframe
        except Exception as ex:
            print(f"Error reading csv file: {ex}")
            return pd.DataFrame()


    def task_1(self, dataframe_gym_data: pd) -> pd:
        """
        Read in source dataset to a format usable in later data analysis.
        Aggregate it to hourly precision by summing the usage statistics for each
        gym device during the hour.
        Present 10 first rows of the dataset.
        Returns:
            dataframe: hourly aggregated dataframe
        """

        if dataframe_gym_data.empty is False:
            df_groupby = dataframe_gym_data.\
                groupby([dataframe_gym_data['time'].str.slice(0, 13)]).\
                sum()
            df_hourly = df_groupby.reset_index()
            print("Task 1 : First 10 elements results dataframe.\n")
            print(df_hourly.head(10))
            return df_hourly
        else:
            print(f"Error, dataframe is empty")
            return dataframe_gym_data

    def task_2(self, dataframe: pd) -> None:
        """
        Perform the quality checks on the original dataset.
        Args:
            :param  dataframe: dataframe
        Returns:
            Quality check verification
        """
        print("Analysis done in the original dataset (not aggregated).\n")
        # There are more than 50,000 rows in the dataset
        count_elements = verify_number_elements(dataframe, 50000)
        # There are records from between 2020-04-24 and 2021-05-11
        verify_range_records(dataframe, '2020-04-24', '2021-05-11')
        # All values in the numerical columns are positive
        verify_positive_values(dataframe, count_elements)

    def task_3(self, df_hourly: pd) -> None:
        """
        Analyse the dataset hourly aggregated dataframe
        Args:
            :param  df_hourly: hourly aggregated dataframe
        Returns:
            Dataset analysis
        """
        # What was the most popular device during the tracking period
        # measured by number of minutes used?
        most_popular_device(df_hourly)
        # Did time of day (hour) impact overall popularity of the outdoor gym?
        is_hour_impacting_popularity(df_hourly)
        # Was the gym more popular overall on weekends (Saturday and Sunday)
        # than on weekdays?
        popularity_gym_weekends_weekdays(df_hourly)

    def task_4(self, df_hourly: pd) -> pd:
        """
        Add new features to the hourly aggregated dataframe.
        •	Weekday as number
        •	Hour as number
        •	Sum of minutes across all gym devices
        Args:
            :param  df_hourly: hourly aggregated dataframe
        Returns:
            df_hourly: original dataframe with new added features
        """
        # Weekday column already added in the previous task
        df_hourly['Hour'] = df_hourly.apply(lambda x: int((x['time'])[11:14]), axis=1)
        df_hourly['sum_minutes'] = df_hourly.apply(lambda x: x['19'] + x['20'] +
                                                             x['21'] + x['22'] +
                                                             x['23'] + x['24'] +
                                                             x['25'] + x['26'], axis=1)
        print("Task 4 : First 10 elements for dataframe with new features "
              "(Hour, Weekday, sum_minutes).\n")
        print(df_hourly.head(10))
        return df_hourly

    def task_5(self, df_hourly_new_features: pd, dataframe_weather_data: pd)-> pd:
        """
        Analyse the impact of weather on gym popularity
        •	Does temperature impact gym popularity?
        •	What about precipitation?
        Args:
            :param  df_hourly_new_features: hourly aggregated dataframe
            :param  dataframe_weather_data: hourly weather dataframe
        Returns:
            Impact temperature and precipitation in gym usage
        """
        # Creating Year, Month, Day columns
        df_hourly_new_features['Year'] = df_hourly_new_features.\
            apply(lambda x: int(x['time'][0:4]), axis=1)
        df_hourly_new_features['Month'] = df_hourly_new_features.\
            apply(lambda x: int(x['time'][5:7]), axis=1)
        df_hourly_new_features['Day'] = df_hourly_new_features.\
            apply(lambda x: int(x['time'][8:10]), axis=1)
        # Converting Hour string to integer
        dataframe_weather_data['Hour'] = dataframe_weather_data.\
            apply(lambda x: int(x['Hour'][0:2]), axis=1)
        # Join by Year, Month, Day, Hour
        df_merged_data = df_hourly_new_features.\
            merge(dataframe_weather_data, on=['Year', 'Month', 'Day', 'Hour'])

        # Temperature analysis
        df_usage_temperature = df_merged_data[["time", "sum_minutes", "Temperature (degC)"]]
        df_usage_temperature.plot(kind='line', x='Temperature (degC)', y='sum_minutes', color='red')
        plt.savefig('./images/usage_gym_temperature.png')
        print("Task 5 : Temperature has impact in the usage of the gym, \n"
              "as the temperature increase also the usage of the gym is more frequent. \n"
              "In images/usage_gym_temperature.png is expressed graphically this trend.\n")

        # Precipitation analysis
        df_usage_precipitation = df_merged_data[["time", "sum_minutes", "Precipitation (mm)"]]
        df_groupby_precipitation = df_usage_precipitation.\
            groupby([df_usage_precipitation['Precipitation (mm)']]).\
            sum().reset_index()
        df_groupby_precipitation.plot(kind='line', x='Precipitation (mm)',
                                      y='sum_minutes', color='blue')
        plt.savefig('./images/usage_gym_precipitation.png')
        print("Task 5 : Precipitation also has impact in the usage of the gym, \n"
              "meanwhile there is few mm (precipitation), the usage of gym has high values. \n"
              "As soon as precipitation increase, the usage of gym is reduced drastically. \n"
              "There is not information about no precipitation (-1) and \n"
              "it was not possible to obtain any conclusion. \n"
              "In the below table and in images/usage_gym_temperature.png \n"
              "is expressed graphically the impact of precipitation.\n")
        print(df_groupby_precipitation)
        return df_merged_data

    def task_6(self, df_merged_data: pd):
        """
        Load the model and add predictions produced by the model as a new attribute to the dataset.
        Args:
            :param  df_merged_data:  dataframe with all the required features used by the model.
        Returns:
            Analysis inference of the model.
        """
        df_merged_data.rename(
            columns={'Weekday': 'weekday', 'Hour': 'hour', 'sum_minutes': 'y'}, inplace=True)
        dataset = df_merged_data[["weekday", "hour", "Precipitation (mm)" ,
                                  "Snow depth (cm)", "Temperature (degC)", "y"]]
        # Clean dataset from null values
        clean_dataset = dataset[dataset.notnull().all(1)]
        # Create test set
        x_values = clean_dataset[["weekday", "hour", "Precipitation (mm)" ,
                                  "Snow depth (cm)", "Temperature (degC)"]]
        y_values = clean_dataset[["y"]]
        # Create prediction on the x_values test set
        predictions = self.model.predict(x_values)
        # Get metrics for the test set
        score = self.model.score(x_values, y_values)
        # Add predictions to the x_values
        x_values['prediction'] = predictions.tolist()
        print("Task 6 : Here is the inference of the model applied to the test set.\n")
        print(x_values)
        print("The results does not look believable since the score is 0.13, \n"
              "it is low but maybe some data normalization was considered "
              "during the building of the model \n"
              "which it is not being considered here.\n")
        print(f"score: {score}")



if __name__ == "__main__":
    logging.info("Outdoor Gym Analysis")
    path_gym_data = os.getenv("PATH_GYM_DATA", "./data/hietaniemi-gym-data.csv")
    path_weather_data = os.getenv("PATH_WEATHER_DATA", "./data/kaisaniemi-weather-data.csv")
    OGA = OutdoorGymAnalysis()
    dataframe_gym_data = OGA.read_csv_data(path_gym_data)
    dataframe_weather_data = OGA.read_csv_data(path_weather_data)
    print("======================================= TASK 1 =======================================")
    df_hourly = OGA.task_1(dataframe_gym_data)
    print("======================================= TASK 2 =======================================")
    OGA.task_2(dataframe_gym_data)
    print("======================================= TASK 3 =======================================")
    OGA.task_3(df_hourly)
    print("======================================= TASK 4 =======================================")
    df_hourly_new_features = OGA.task_4(df_hourly)
    print("======================================= TASK 5 =======================================")
    df_merged_data = OGA.task_5(df_hourly_new_features, dataframe_weather_data)
    print("======================================= TASK 6 =======================================")
    OGA.task_6(df_merged_data)
