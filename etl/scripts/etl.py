# -*- coding: utf-8 -*-

import os
import os.path as osp

import zipfile
from io import BytesIO

import pandas as pd

from ddf_utils.factory import ihme
from ddf_utils.str import format_float_digits


source_dir = '../source/'
out_dir = '../../'


def read_source():
    res = list()
    for f in os.listdir(source_dir):
        if f.startswith('IHME') and f.endswith('zip'):
            print(f)
            try:
                zf = zipfile.ZipFile(osp.join(source_dir, f))
            except zipfile.BadZipFile:
                print(f'{f} is broken, please re-run download script')
                raise
            csvf = zf.namelist()[0]
            f = BytesIO(zf.read(csvf))
            res.append(pd.read_csv(f))
    if len(res) > 1:
        return pd.concat(res, ignore_index=True)
    return res[0]


def main():
    print('reading source files...')
    data = read_source()
    print('reading metadata...')
    md = ihme.load_metadata()

    print('creating ddf...')
    data = data.drop(['measure', 'metric'], axis=1)  ## measure and metric are fixed
    data = data.set_index(['location', 'sex', 'age', 'year'])
    data = data.sort_index()
    data = data.rename(columns={'val': 'mean'})

    # datapoints
    for c in data.columns:
        data[c] = data[c].map(format_float_digits)
        data[[c]].to_csv(osp.join(out_dir,
                                  'ddf--datapoints--{}--by--location--sex--age--year.csv'.format(c)))

    str_concepts = set()

    # entities
    for e in ['location', 'sex', 'age']:
        edf = md[e]
        if e == 'location':
            edf = edf[edf.location_id != 'custom'].drop('location_id', axis=1)
            edf['id'] = edf['id'].map(int)
        edf = edf.rename(columns={'id': e})
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
