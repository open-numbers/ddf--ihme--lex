# Life expectancy from IHME

source: [link](https://cloud.ihme.washington.edu/index.php/s/b89390325f728bbd99de0356d3be6900/download?path=%2F&files=IHME_GBD_2013_LIFE_EXPECTANCY_1970_2013_Y2014M12D17.zip)

# Note for 2014 version of data

the codebook contains error that 2 countries names are missing
and other countries names are shifted up 2 rows in the codebook.

The etl script will check if country data are same in codebook and data file.
If it fails to run, please double check the country data in codebook and data file.
