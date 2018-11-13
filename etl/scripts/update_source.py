# -*- coding: utf-8 -*-


import os
import tempfile
import shutil

from ddf_utils.factory import ihme


source_dir = '../source'


def remove_old_source():
    for f in os.listdir(source_dir):
        if f.startswith('IHME') and f.endswith('zip'):
            os.remove(os.path.join(source_dir, f))


def main():
    md = ihme.load_metadata()
    latest = md['version'].sort_values(by='id').iloc[-1, 0]
    print('latest version is: {}'.format(latest))

    tmp_dir = tempfile.mkdtemp()
    folders = ihme.bulk_download(tmp_dir, latest, 'le')
    if not folders:
        print('download was not completed.')
        raise ValueError('downloader failed')

    remove_old_source()

    # there should be one folder
    folder = os.path.join(tmp_dir, folders[0])
    for f in os.listdir(folder):
        if f.startswith('IHME') and f.endswith('zip'):
            shutil.move(os.path.join(folder, f), source_dir)
    print('downloaded.')


if __name__ == '__main__':
    main()
