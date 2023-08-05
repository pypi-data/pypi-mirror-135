import pandas as pd

class OneHotEncoding:
    def __init__(self, target_column:str):
        self.target_column = target_column
    def perform_one_hot_encoding(self, dataframesource):
        # Get one hot encoding of column
        one_hot_column_encoding = pd.get_dummies(dataframesource[self.target_column])
        # Drop column as it is now encoded
        dataframesource = dataframesource.drop(self.target_colum,axis = 1)
        # Join the encoded df
        dataframesource = dataframesource.join(one_hot_column_encoding)
        return dataframesource