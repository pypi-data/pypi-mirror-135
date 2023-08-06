# shot_point_scraper　

"shot_point_scraper" is a library for scraping shot positions and their information for one game from [Understat](https://understat.com/). 

# Features
 
shot_point_scraper supports csv files, excel files, and sql files as output file formats.
 
# Requirement
 
* python 3.9
* beautifulsoup4 4.10.0
* pandas 1.3.5
* openpyxl 3.0.9
* requests 2.27.1
* lxml
 
# Installation
 
 Install shot_point_scraper with pip command.
 
```zsh
pip install shotpointscraper
```
 
# Usage
 
 1. Check the ID of the match you want to retrieve from [Understat](https://understat.com/)
   ID You can check the ID of the match in the URL section.(https://understat.com/match/ID)

 2.In the environment where shot_point_scraper is installed, execute the following command

   ```zsh
     shotpointscraper
   ```
  3.You will be asked for your ID, so fill in the ID that you just checked.

 4.When scraping is finished, you will be asked what file you want to create, so enter the file you want to create (csv excel,sql).

 5.If you select csv or excel, you will be asked for a file name, please enter your file name of choice. (Do not enter the file format, as it will be added automatically.)
 The file will then be generated.

 6.If you choose "sql", you will be asked what format you would like the  shoot position information to be in.
   xy: Describe the chute coordinates using two columns, x and y.
   point: Write the chute coordinates in one column using commas and parentheses for x and y.

example:
 xy:
|  x  |  y  |
| ---- | ---- |
|  112.07  |  43.4  |
|  115.15  |  38.9  |

 point:
|  point  |
| ---- |
|  (112.07,43.4)  |
|  (115,15,38.9)  |
    
 7.You will be asked for the name of the file to be generated and the name of the database table to be filled in the sql file.
 The file will then be generated.

# Note
 
I don't test environments under Linux and Windows.

For the shoot position information, I use the statbomb type.(0<=x<=120,0<=y<=80)
 
# Author

* Daiki Azuma 
* Musashino University
* Twitter : https://twitter.com/comfused_azuma

# License
 
"shot_point_scraper" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

I hope this library will be useful to you.
Thank you!
