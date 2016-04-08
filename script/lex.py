# -*- coding: utf-8 -*-
"""transform the life expectancy data from IHME to DDF data model."""

import pandas as pd
from index import create_index_file

# configuration of file path.
# code book contains all concepts and entities in the data set.
codebook_csv = '../source/IHME_GBD_2013_LIFE_EXPECTANCY_1970_2013_Y2014M12D17/IHME_GBD_2013_LIFE_EXPECTANCY_1970_2013_CB_Y2014M12D17.CSV'
data_csv = '../source/IHME_GBD_2013_LIFE_EXPECTANCY_1970_2013_Y2014M12D17/IHME_GBD_2013_LIFE_EXPECTANCY_1970_2013_Y2014M12D17.CSV'
out_dir = '../output/'


# functions for building ddf
def extract_concept_discrete(codebook):
    """extract discrete concepts from codebook"""

    # get all concepts and names
    dis_concept = codebook.ix[:1].T.ix[:10]
    dis_concept = dis_concept.drop(9)  # drop the concept "Metric", not used any where.

    # fill the columns: concept/name/type
    dis_concept.columns = ['concept', 'name']
    dis_concept['type'] = 'string'
    dis_concept['type'].ix[[1, 5, 7]] = 'entity_domain'
    dis_concept['type'].ix[4] = 'time'

    return dis_concept


def extract_concept_continuous(codebook):
    """extract continuous concepts from codebook"""

    # get all concepts and names
    cont_concept = codebook.ix[:1].T.ix[11:]

    # fill the columns: concept/name/type/unit
    cont_concept.columns = ['concept', 'name']
    cont_concept['type'] = 'measure'
    cont_concept['unit'] = 'years'

    return cont_concept


def extract_entities_country(codebook):
    """extract country entities from codebok"""

    # get all columns for country
    ent_country = codebook.ix[:, :3]

    # reset the columns
    ent_country.columns = ent_country.ix[0]
    ent_country = ent_country.drop([0, 1])
    ent_country = ent_country.dropna(how='all')

    return ent_country


def extract_entities_age_group(codebook):
    """extract age group entities from codebok"""

    ent_age = codebook.ix[:, 5:6]
    ent_age = ent_age.dropna(how='all')
    ent_age.columns = ent_age.ix[0]
    ent_age = ent_age.drop([0, 1])

    return ent_age


def extract_entities_sex(codebook):
    """extract sex entities from codebok"""

    ent_sex = codebook.ix[:, 7:8]
    ent_sex = ent_sex.dropna(how='all')
    ent_sex.columns = ent_sex.ix[0]
    ent_sex = ent_sex.drop([0, 1])

    return ent_sex

'''
because it's very straight forward to extract datapoints, I won't write
functions here.
'''

if __name__ == '__main__':
    import os

    print('reading source files...')
    codebook = pd.read_csv(codebook_csv, skiprows=1, header=None)
    codebook = codebook.iloc[:, 1:]  # remove unnecessary column
    data = pd.read_csv(data_csv)

    print('creating concept files...')
    discrete = extract_concept_discrete(codebook)
    discrete.to_csv(os.path.join(out_dir, 'ddf--concepts--discrete.csv'), index=False)

    continuous = extract_concept_continuous(codebook)
    continuous.to_csv(os.path.join(out_dir, 'ddf--concepts--continuous.csv'), index=False)

    print('creating entities files...')
    country = extract_entities_country(codebook)
    country.to_csv(os.path.join(out_dir, 'ddf--entities--location_id.csv'), index=False)

    age = extract_entities_age_group(codebook)
    age.to_csv(os.path.join(out_dir, 'ddf--entities--age_group_id.csv'), index=False)

    sex = extract_entities_sex(codebook)
    sex.to_csv(os.path.join(out_dir, 'ddf--entities--sex_id.csv'), index=False)

    print('creating data points files...')
    mean = data.ix[:, [0, 3, 4, 6, 10]]
    upper = data.ix[:, [0, 3, 4, 6, 11]]
    lower = data.ix[:, [0, 3, 4, 6, 12]]

    mean.to_csv(os.path.join(
        out_dir,
        'ddf--datapoints--mean--by--location_id--age_group_id--sex_id--year.csv'), index=False)
    upper.to_csv(os.path.join(
        out_dir,
        'ddf--datapoints--upper--by--location_id--age_group_id--sex_id--year.csv'), index=False)
    lower.to_csv(os.path.join(
        out_dir,
        'ddf--datapoints--lower--by--location_id--age_group_id--sex_id--year.csv'), index=False)

    print('generating index file...')
    create_index_file(out_dir, os.path.join(out_dir, 'ddf--index.csv'))
