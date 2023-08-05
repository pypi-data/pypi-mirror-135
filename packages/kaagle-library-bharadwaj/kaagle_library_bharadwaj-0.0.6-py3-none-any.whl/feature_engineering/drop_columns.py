import pandas as pd

class DropColumns:
    
    def __init__(self, columnslist):
        self.dropcolumnslist = columnslist
        
    def drop_columns_from_dataframe(self, dataframesource):
        for dropcolumn in self.dropcolumnslist:
            dataframesource.drop(dropcolumn, axis=1, inplace=True)
        return dataframesource