import argparse

from .s3_gateway import create as create_s3_gateway


if __name__ == '__main__':
    s3_gateway = create_s3_gateway()

    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()

    # TODO: this obviously should be changed, needed to parametrize the bucket name
    s3_gateway.upload(file_path=args.path, bucket_name='backmeup-bucket')
