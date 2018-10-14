import argparse
import logging
from back_me_up import create as create_back_me_up

logging.basicConfig(format='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    back_me_up = create_back_me_up()

    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='Bucket name where the file is going to be stored in S3')
    parser.add_argument('path', help='Path to file should be uploaded to S3')

    args = parser.parse_args()

    try:
        logger.info('Starting to upload file(s)')
        back_me_up.sync(args.bucket_name, args.path)
        logger.info(f'\'{args.path}\' was uploaded successfully to \'{args.bucket_name}\'')
    except Exception as e:
        logger.error(f'The following error was raised while trying to upload \'{args.path}\' to \'{args.bucket_name}\': \n\n\"{e}\"')
