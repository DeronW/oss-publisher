import sys
import os
import settings
import oss2

BUCKET = None
COVER = False
SEAT = './seat/'
DIRECTORY = None

success_files = []
covered_files = []
duplicated_files = []
failed_files = []

for i in sys.argv:
    if i == '--cover':
        COVER = True
    if i.startswith('--dir='):
        DIRECTORY = i[6:]

def config(CONFIG):
    auth = oss2.Auth(CONFIG['id'], CONFIG['key'])
    global BUCKET
    BUCKET = oss2.Bucket(auth, 'http://' + CONFIG['host'], CONFIG['bucket'])

def sync():
    if DIRECTORY is None:
        raise '--dir=??? parameter is required'

    keys = []
    for root, dirs, files in os.walk(SEAT):
        for name in files:
            k = os.path.join(root, name).replace(SEAT, '', 1)
            keys.append(k)

    for key in keys:
        if check(key):
            upload(key)

def check(key):
    global duplicated_files

    if BUCKET.object_exists(key):
        if COVER:
            covered_files.append(key)
        else:
            duplicated_files.append(key)
            return False
    return True

def upload(key):
    global success_files
    global failed_files

    if BUCKET.put_object_from_file(key, os.path.join(SEAT, key)):
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

    print('covered files: %s' % len(covered_files))
    echo(covered_files)

    print('duplicated and ignored files: %s' % len(duplicated_files))
    echo(duplicated_files)

    print('failed files: %s' % len(failed_files))
    echo(failed_files) 

if __name__ == '__main__':
    config(settings.QA_CN)
    # traverse_files()
    sync()
    show_log()
