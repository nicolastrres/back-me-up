import argparse

from .s3_gateway import create as create_s3_gateway


if __name__ == '__main__':
    s3_gateway = create_s3_gateway()

    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='Bucket name where the file is going to be stored in S3')
    parser.add_argument('path', help='Path to file should be uploaded to S3')

    args = parser.parse_args()

    try:
        s3_gateway.upload(file_path=args.path, bucket_name=args.bucket_name)
    except Exception as e:
        print(f'The following error was raised while trying to upload \'{args.path}\' to \'{args.bucket_name}\': \n\n\"{e}\"')
