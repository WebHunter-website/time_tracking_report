# Time tracking report

## About
This script creates HTML email message with summary table of time worked in given month every week. Input data are in form of CSV file exported from Google Sheets.

## Requirements
  * Python 3+

## Setup
Recommended way to use `time_tracking_report` is to create Python virtual environment:
```
python -m venv .\venv
```
and install project required packages:
```
.\venv\Scripts\python.exe -m pip install -r .\requirements.txt
```

### Expected input
Google Sheets document should be of structure:
![Google Sheets table setup](/source/images/google_sheets_print_screen.png)

### Important notes
  * Every week must begin with **Sunday** and end with **Saturday**
  * Before using data must be downloaded as CSV
  ![Google Sheet CSV export](/source/images/google_sheets_print_screen_2.png)
  * Script is using **current date** to fetch data from CSV file so it is necessary to generate report the same month data are related to.

## Example
Execute script:
```
.\venv\Scripts\python.exe .\time_tracking_report.py
```
enter path to downloaded CSV file and hit enter. generated HTML will be automatically saved to the clipboard (ready to paste it).

HTML template can be edited in script content.
