This is a Python script that scrapes the latest data regarding the **COVID-19** pandemic in Romania
from the [datelazi.ro](https://datelazi.ro) website via the JSON interface and reformats the data into a CSV file.

** Known issues **
The number of confirmed cases for the start date of the data (17-03-2020) is **NOT** the correct
number of cases for the day, it is a placeholder so the total number of confirmed cases is correct
(when computing the sum up to the present day). 