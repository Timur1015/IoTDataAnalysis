import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.classes.IoTStandardPlotter import IoTStandardPlotter


class Utility:

    def __init__(self):
        pass

    @staticmethod
    def convert_to_ts(data: pd.DataFrame,index_name: str):
        data[index_name] = pd.to_datetime(data[index_name])
        data.set_index(index_name, inplace=True)
        data.sort_index(inplace=True)

    @staticmethod
    def scale_data(data: pd.DataFrame):
        sc = StandardScaler().set_output(transform='pandas')
        return sc.fit_transform(data)

    @staticmethod
    def filter_by_months(data: pd.DataFrame, num_months):
        last_timestamp = data.index.max()
        interval = last_timestamp - pd.DateOffset(months=num_months)
        return data.loc[interval:]

    @staticmethod
    def spit_into_months(data: pd.DataFrame):
        return [group for _, group in data.groupby(pd.Grouper(freq='ME'))]

    @staticmethod
    def calc_mean(data: pd.DataFrame):
        return data.dropna().mean()

    @staticmethod
    def get_month_name(data: pd.DataFrame):
        m = data.index.min().month
        month_name = ''
        if m == 5:
            month_name = 'May'
        if m == 6:
            month_name = 'June'
        if m == 7:
            month_name = 'July'
        return month_name

