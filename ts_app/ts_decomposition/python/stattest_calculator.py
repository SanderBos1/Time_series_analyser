import pymannkendall as mk
import pandas as pd
import matplotlib.pyplot as plt
from flask import current_app
from scipy import stats
from statsmodels.tsa.stattools import adfuller

plt.switch_backend("agg")


class trend_calculator:

    def __init__(self, variable_dict):
        """
        Initializes the TrendCalculator.

        Parameters:
        - variable_dict (dict): A dictionary containing keys 'dataset', 'var_column', and 'trend_function'.
          'dataset': The file path of the dataset.
          'var_column': The name of the column in the dataset for trend analysis.
          'trend_function': The statistical function to use for trend analysis.
        """
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.trend = variable_dict["trend_function"]

    def _calculate_mann_kendall_trend(self):
        """
        Calculates the trend using the Mann-Kendall method.

        Returns:
        - p_value (float): The p-value indicating the significance of the trend.

        """
        p_value = mk.original_test(self.df[self.column]).p
        return p_value

    def calculate_trend(self):
        """
        Calculates the trend based on the specified function.

        Returns:
        - float: The p-value indicating the significance of the trend, rounded to 4 decimal places.

        Raises:
        - KeyError: If the specified column is not found in the dataset.
        - FileNotFoundError: If the dataset file is not found.
        - ValueError: If an error occurs during trend calculation or if an invalid trend function is specified.
        """
        try:
            self.df[self.column] = pd.to_numeric(self.df[self.column], errors="coerce")
            if self.trend == "pymannkendall":
                p_value = self._calculate_mann_kendall_trend()
                return round(p_value, 4)
            else:
                raise ValueError("Invalid trend function specified.")
        except KeyError as e:
            raise KeyError(
                f"Column '{self.var_column}' not found in the dataset."
            ) from e
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Dataset '{self.dataset_path}' not found.") from e
        except Exception as e:
            raise ValueError("An error occurred during trend calculation.") from e


class seasonality_calculator:
    """
    A class for calculating seasonality in datasets using different statistical methods.

    Attributes:
    - df (pd.DataFrame): The DataFrame containing the dataset.
    - column (str): The name of the column in the dataset for seasonality analysis.
    - function (str): The statistical function to use for seasonality analysis.
    - period (str): The period over which seasonality is analyzed (e.g., 'year' or 'month').
    - time_column (str): The name of the column in the dataset containing time information.

    Methods:
    - __init__(variable_dict): Initializes the SeasonalityCalculator with the dataset and parameters.
    - kruskal_wallis(): Performs seasonality analysis using the Kruskal-Wallis test.
    - calculate_seasonality(): Calculates seasonality based on the specified function.
    """

    def __init__(self, variable_dict):
        """
        Initializes the SeasonalityCalculator.

        Parameters:
        - variable_dict (dict): A dictionary containing keys 'dataset', 'var_column', 'seasonality_function', 'period'.
          'dataset': The file path of the dataset.
          'var_column': The name of the column in the dataset for seasonality analysis.
          'seasonality_function': The statistical function to use for seasonality analysis.
          'period': The period over which seasonality is analyzed (e.g., 'year' or 'month').
        """
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.function = variable_dict["seasonality_function"]
        self.period = variable_dict["period"]
        self.time_column = current_app.config["TIME_COLUMN"]

    def kruskal_wallis(self):
        """
        Performs seasonality analysis using the Kruskal-Wallis test.

        Returns:
        - p_value (float): The p-value indicating the significance of seasonality.
        """
        if self.period.lower() == "year":
            grouped_df = self.df.groupby(
                pd.Grouper(key=self.time_column, freq="1YE")
            ).mean()
        elif self.period.lower() == "month":
            grouped_df = self.df.groupby(
                pd.Grouper(key=self.time_column, freq="1M")
            ).mean()
        p_value = stats.kruskal(*grouped_df[self.column].values).pvalue
        return p_value

    def calculate_seasonality(self):
        """
        Calculates seasonality based on the specified function.

        Returns:
        - float: The p-value indicating the significance of seasonality, rounded to 4 decimal places.
        """
        self.df[self.time_column] = pd.to_datetime(self.df[self.time_column])
        self.df[self.column] = pd.to_numeric(self.df[self.column], errors="coerce")
        if self.function == "kruskal":
            p_value = self.kruskal_wallis()
        return round(p_value, 4)


class stationarity_calculator:
    """
    A class for calculating stationarity in datasets using different statistical methods.

    Attributes:
    - df (pd.DataFrame): The DataFrame containing the dataset.
    - column (str): The name of the column in the dataset for stationarity analysis.
    - function (str): The statistical function to use for stationarity analysis.
    - time_column (str): The name of the column in the dataset containing time information.

    Methods:
    - __init__(variable_dict): Initializes the StationarityCalculator with the dataset and parameters.
    - adfuller(): Performs stationarity analysis using the Augmented Dickey-Fuller test.
    - calculate_seasonality(): Calculates stationarity based on the specified function.
    """

    def __init__(self, variable_dict):
        """
        Initializes the StationarityCalculator.

        Parameters:
        - variable_dict (dict): A dictionary containing keys 'dataset', 'var_column', and 'stationarity_function'.
          'dataset': The file path of the dataset.
          'var_column': The name of the column in the dataset for stationarity analysis.
          'stationarity_function': The statistical function to use for stationarity analysis.
        """
        self.df = pd.read_csv(variable_dict["dataset"])
        self.column = variable_dict["var_column"]
        self.function = variable_dict["stationarity_function"]
        self.time_column = current_app.config["TIME_COLUMN"]

    def adfuller(self):
        """
        Performs stationarity analysis using the Augmented Dickey-Fuller test.

        Returns:
        - p_value (float): The p-value indicating the significance of stationarity.
        """
        result = adfuller(self.df[self.column])
        p_value = result[1]
        return p_value

    def calculate_seasonality(self):
        """
        Calculates stationarity based on the specified function.

        Returns:
        - float: The p-value indicating the significance of stationarity, rounded to 4 decimal places.
        """
        self.df[self.time_column] = pd.to_datetime(self.df[self.time_column])
        self.df[self.column] = pd.to_numeric(self.df[self.column], errors="coerce")
        if self.function == "adfuller":
            p_value = self.adfuller()
        return round(p_value, 4)
