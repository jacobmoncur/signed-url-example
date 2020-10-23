import boto3
from flask import Flask, request, redirect
import jwt
import os

app = Flask(__name__)

secret = os.environ['SECRET']

s3_client = boto3.client('s3', endpoint_url = 'https://s3.us-west-000.backblazeb2.com')

def generate_presigned_url(jwt):
    url = s3_client.generate_presigned_url(ClientMethod='get_object', Params={
        'Bucket': jwt['bucket'], 'Key': jwt['key']}, ExpiresIn='3600')
    return url


@app.route('/')
def pull_url():
    encoded = request.args.get('token')
    decoded = "Please provide a valid JWT in your URL. This may mean that you used the wrong secret in the AWS console."
    try:
        decoded = jwt.decode(encoded, secret, algorithms=['HS256'])
    except:
        return decoded

    generated_url = generate_presigned_url(decoded)
    return redirect(generated_url)


if __name__ == '__main__':
    app.run()
