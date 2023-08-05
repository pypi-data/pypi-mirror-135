import pandas as pd

class FillNa:
    def __init__(self, column_name:str):
        self.column_name = column_name
    def populate_na_values(self, dataframesource, fill_na_value):
        dataframesource[self.column_name].fillna(value=fill_na_value, inplace=True)
        return dataframesource