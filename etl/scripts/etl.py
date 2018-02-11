# -*- coding: utf-8 -*-

import os
import os.path as osp

import zipfile
from io import BytesIO

import pandas as pd

from ddf_utils.factory import ihme


source_file = '../source/DATA.zip'
out_dir = '../../'


def read_source():
    zf = zipfile.ZipFile(source_file)
    csvf = zf.namelist()[0]
    f = BytesIO(zf.read(csvf))

    return pd.read_csv(f)


def main():
    print('reading source files...')
    data = read_source()
    print('reading metadata...')
    md = ihme.load_metadata()

    print('creating ddf...')
    data = data.drop(['measure', 'metric'], axis=1)  ## measure and metric are fixed
    data = data.set_index(['location', 'sex', 'age', 'year'])
    data = data.rename(columns={'val': 'mean'})

    # datapoints
    for c in data.columns:
        data[[c]].to_csv(osp.join(out_dir,
                                  'ddf--datapoints--{}--by--location--sex--age--year.csv'.format(c)))

    str_concepts = set()

    # entities
    for e in ['location', 'sex', 'age']:
        edf = md[e]
        edf = edf.rename(columns={e+'_id': e})
        edf = edf.set_index(e)

        for c in edf.columns:
            str_concepts.add(c)
            edf.to_csv(osp.join(out_dir,
                                'ddf--entities--{}.csv'.format(e)))

    # concepts
    concepts = {}
    concepts['measure'] = data.columns.values
    concepts['entity_domain'] = ['location', 'sex', 'age']

    concepts['string'] = list(str_concepts)
    concepts['time'] = ['year']
    clist = []

    for k, v in concepts.items():
        for v_ in v:
            clist.append({'concept': v_, 'concept_type': k})

    cdf = pd.DataFrame.from_records(clist)
    cdf.to_csv(osp.join(out_dir,
                        'ddf--concepts.csv'), index=False)

    print('Done.')


if __name__ == '__main__':
    main()
