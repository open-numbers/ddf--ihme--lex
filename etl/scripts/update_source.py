# -*- coding: utf-8 -*-


import os
import shutil

from ddf_utils.factory import ihme


source_dir = '../source'


def main():
    md = ihme.load_metadata()
    latest = md['version'].sort_values(by='version_id').iloc[-1, 0]
    print('latest version is: {}'.format(latest))

    ihme.bulk_download(source_dir, latest, 'le')
    for f in os.listdir(source_dir):
        # FIXME: deal with multiple data
        if f.startswith('IHME') and f.endswith('zip'):
            shutil.move(os.path.join(source_dir, f), os.path.join(source_dir, 'DATA.zip'))
            break
    print('downloaded.')


if __name__ == '__main__':
    main()
