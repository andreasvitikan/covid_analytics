COVID-19 GCS (România) data scraper and parser
==============================================

This is a Python script that scrapes the latest official data regarding the **COVID-19** pandemic in [Romania](https://stirioficiale.ro/informatii)
from the [datelazi.ro](https://datelazi.ro) website via the JSON interface. The script computes the daily changes
for the total number of confirmed positive cases, total number of deaths and total number of cured patients.

The script also computes the daily changes for the total number of confirmed positive cases
by age group (labeled `distributionByAge`) and by county (labeled `countyInfectionsNumbers`).
The data is then exported in a CSV file (separator = `,`) with a header first row (the *age* groups
are prefixed with **age**: `age0-9, age9-19`, etc. and the **county** numbers are prefixed with
*county*: `countyAB, countyAR`, etc.) and with the subsequent rows containing the computed data.

The dates, as exported in the CSV file, are formatted in the same way as in the original JSON file,
namely: `YYYY-mm-dd` or `%Y-%m-%d` (for `strftime()`).

Known issues
------------

1. The number of confirmed cases for the start date of the data (17-03-2020) is **NOT** the daily changes
in cases for the day, it is the total cases up to that day, so the total number of confirmed cases is correct
(when computing the sum up to the present day).

2. For data before **2020-04-03** (April 3rd, 2020), where countyInfectionsNumbers are not available, the values for the county columns
are padded with 0 in order to keep the number of values per row constant. 
