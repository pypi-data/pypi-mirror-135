import boto3
from botocore.exceptions import ClientError


class S3Client:
    def __init__(self, bucket_name: str, region: str):
        self._bucket_name = bucket_name
        self._region = region
        self._client = boto3.resource('s3')

    def _ensure_bucket(self):
        try:
            _ = self._client.create_bucket(
                ACL='private',
                Bucket=self._bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self._region
                }
            )
        except ClientError:
            pass

    def upload(self, data, filename):
        self._ensure_bucket()
        obj = self._client.Object(self._bucket_name, filename)
        response = obj.put(Body=data)

        return response

    def read(self, filename):
        return self._client.Object(self._bucket_name, filename).get()['Body'].read()
