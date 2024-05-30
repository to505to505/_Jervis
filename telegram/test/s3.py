import boto3

# Set up AWS credentials and region
aws_access_key_id = 'AKIAQME5MYJPO377UW6W'
aws_secret_access_key = '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'
region_name = 'eu-north-1'
output = 'json'
bucket_name = 'jervis-reference'

# Create an S3 client (configuration)
s3 = boto3.client('s3',
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key,
                  region_name=region_name
                  )




# Upload the file to S3
def upload_s3(photo_name, upload_path):
    object_key = photo_name
    with open(upload_path, "rb") as f:
        s3.upload_fileobj(f, bucket_name, object_key)

#EXAMPLE - Uploading file to s3 with name 'file_new.jpg' 
upload_s3('file_new1.jpg', '/Users/dmitrysakharov/Downloads/2023-05-01 16.13.23.jpg')
upload_s3('file_new2.jpg', '/Users/dmitrysakharov/Downloads/2023-05-01 16.13.23.jpg')
upload_s3('file_new3.jpg', '/Users/dmitrysakharov/Downloads/2023-05-01 16.13.23.jpg')
print('done')


# Downloading the file from S3
def download_s3(photo_name, download_path):
    object_key = photo_name
    local_file_path = download_path+object_key
    s3.download_file(bucket_name, object_key, local_file_path)

#EXAMPLE - Downloading file from s3 with name 'file1.jpg' (там должен быть олимпийский флаг)
#download_s3('file_new.jpg', '/Users/dmitrysakharov/Documents/_Jervis/telegram/app/reference/')
