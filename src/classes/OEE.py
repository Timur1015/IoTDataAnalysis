import pandas as pd
from ressources.Data import Data


class OEE:
    def __init__(self):
        self._df = pd.read_csv(Data.OEE.value)

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, val):
        self._df = val
