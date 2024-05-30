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


key = 'photo_2023-04-16 19.54.29.jpeg'



url = s3.get_object_attributes(
    ClientMethod='get_object',
    Params={
        'Bucket': bucket_name,
        'Key': key,
    },
    ExpiresIn=3600  # link expires in 1 hour
)

print(url)
