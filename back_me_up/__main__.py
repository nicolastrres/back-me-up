import argparse
from back_me_up import create as create_back_me_up
from .logs import get_logger

logger = get_logger(__name__)


if __name__ == '__main__':
    back_me_up = create_back_me_up()

    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name', help='Bucket name where the file is going to be stored in S3')
    parser.add_argument('path', help='Path to file should be uploaded to S3')

    args = parser.parse_args()

    try:
        logger.info('Starting to upload file(s)')
        back_me_up.sync(args.bucket_name, args.path)
    except Exception as e:
        logger.error(
            f'The following error was raised while trying to upload '
            f'\'{args.path}\' to \'{args.bucket_name}\': \n\n\"{e}\"'
        )
