import boto3
from pprint import pprint
import pathlib
import os

def upload_file_using_client():
    """
    Uploads file to S3 bucket using S3 client object
    :return: None

    S3 Bucket location: 
     s3://famlive/sample_upload/

    """
    s3 = boto3.client("s3")
    bucket_name = "famlive"
    bucket_folder = "training_upload"
    object_name = "sample_file_Lucas_v2.txt"
    file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file_Lucas_v2.txt")

    response = s3.upload_file(file_name, bucket_name, '%s/%s' % (bucket_folder,object_name ))
    pprint(response)  # prints None


if __name__ == "__main__":
    upload_file_using_client()
    # upload_file_using_resource()
    # upload_file_to_s3_using_put_object()
    # upload_file_to_s3_using_file_object()