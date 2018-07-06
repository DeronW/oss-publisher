import sys
import os
import settings
import oss2
import shutil

# from IPython import embed

BUCKET = None
COVER = False
DIRECTORY = None
ENV = None
PREFIX = None
DRY_RUN = False
EXCLUDE_EXT = []
ONLY_EXT = []

success_files = []
covered_files = []
duplicated_files = []
failed_files = []
excluded_files = []

for i in sys.argv:
    if i == '--cover':
        COVER = True
    if i.startswith('--dry-run'):
        DRY_RUN = True
    if i.startswith('--dir='):
        DIRECTORY = i[6:]
    if i.startswith('--env='):
        ENV = i[6:]
    if i.startswith('--prefix='):
        PREFIX = i[9:]
    if i.startswith('--only='):
        ONLY_EXT = i[7:].split(',')
    if i.startswith('--exclude='):
        EXCLUDE_EXT = i[10:].split(',')


if ENV is None:
    raise '--env=??? parameter is required'
if DIRECTORY is None:
    raise '--dir=??? parameter is required'

def config(CONFIG):
    auth = oss2.Auth(CONFIG['id'], CONFIG['key'])
    global BUCKET
    BUCKET = oss2.Bucket(auth, 'http://' + CONFIG['host'], CONFIG['bucket'])

def sync():

    global excluded_files

    keys = []
    for root, _, files in os.walk(DIRECTORY):
        for name in files:
            fp = os.path.join(root, name)
            key = PREFIX + fp.replace(DIRECTORY, '', 1)
            keys.append((key, fp))

    for (key, fp) in keys:
        excluded_key = None

        for ext in EXCLUDE_EXT:
            if fp.endswith(ext):
                excluded_key = key

        for ext in ONLY_EXT:
            if not fp.endswith(ext):
                excluded_key = key

        # if a file start with a dot, we should't upload it to OSS
        if key.startsWith('.'):
            excluded_key = key

        if excluded_key:
            excluded_files.append(key)
        else:
            if check(key):
                upload(key, fp)

def check(key):
    global duplicated_files

    if BUCKET.object_exists(key):
        if COVER:
            covered_files.append(key)
        else:
            duplicated_files.append(key)
            return False
    return True

def upload(key, fp):
    global success_files
    global failed_files

    if DRY_RUN or BUCKET.put_object_from_file(key, fp):
        success_files.append(key)
    else:
        failed_files.append(key)

def traverse_files():
    # Traverse all objects in the bucket
    for object_info in oss2.ObjectIterator(BUCKET):
        print(object_info.key)

def show_log():

    def echo(arr):
        for i in arr:
            print('  +', i)

    print('success files: %s' % len(success_files))
    echo(success_files)

    print('excluded files: %s' % len(excluded_files))
    echo(excluded_files)

    print('covered files: %s' % len(covered_files))
    echo(covered_files)

    print('duplicated and ignored files: %s' % len(duplicated_files))
    echo(duplicated_files)

    print('failed files: %s' % len(failed_files))
    echo(failed_files)

def clean():
    path = os.path.join(DIRECTORY)
    shutil.rmtree(path)
    print('Clean up: %s' % path)

def main():
    print("====================================================")
    print("Start publish static files to Ali OSS")
    print("ENV: %s, prefix: %s, cover: %s, dir: %s" % (ENV, PREFIX, COVER, DIRECTORY))
    print("====================================================")
    try:
        config(settings.__getattribute__(ENV))
        # traverse_files()
        sync()
        show_log()
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()

