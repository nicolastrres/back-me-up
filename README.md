# Back me up

Automatically backup folders to different cloud services (S3, Google Drive, Dropbox). It keeps monitoring the files on the folders defined when configured, and when it detects a change on the folder, it automatically update the files on all the services.

# [NOTE]

This readme was written previous the development of the application, so it does not reflect the current status. It was created to guide the development.

## Installation
**Back me** up is distributed on [PyPI](https://pypi.python.org). The best way to install it is with pip:

```
# Create a virtualenvironment (optional, but recommended)
python3 -m venv backmeup-env
source backmeup-env/bin/activate

# Install backmeup
pip install backmeup
```

## Usage

```
backmeup -h

usage: backmeup [-h]

Options:

 --status  Provides deamon status
 --stop  Stop deamon
 --start  Start backing up services
 -t|--time  Frequency with which backmeup will look for changes on the folders to backup
 -f|--folders List of folders to backup, comma-separated
 --gdrive Backup files to google drive folder
 --s3 Backup files to an AWS s3 bucket
 --dropbox Backup files to a dropbox folder
 -E Encrypt all files before sending them to the cloud services.
```

The following example will configure backmeup to look every 5 minutes on the folders `~/Documents` and `~/Images`, if a file changed since the last backup, it will be updated on the services.
```
backmeup --start -t 5 -f ~/Documents ~/Images
```

#### Credentials

Backmeup reads the credentials for the cloud services from the environment variables.
##### TODO: Add more details on the required credentials.




