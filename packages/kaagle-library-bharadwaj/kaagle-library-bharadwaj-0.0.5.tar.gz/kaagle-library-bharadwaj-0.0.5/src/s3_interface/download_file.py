import boto3
import warnings
import pandas as pd

class S3_DownLoadFile:
    
    def __init__(self, bucket_name:str, bucket_key:str):
        self.bucket_name = bucket_name
        self.bucket_key  = bucket_key
    
    def download_file(self, file_name:str):
        s3 = boto3.client('s3')
        warnings.filterwarnings("ignore")
        obj = s3.get_object(Bucket=self.bucket_name, Key=self.bucket_key + file_name)
        df_downloaded_data = pd.read_csv(obj['Body'])
        return df_downloaded_data