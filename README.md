# DACSspace

A simple Python script to evaluate your ArchivesSpace instance for DACS [single-level minimum](http://www2.archivists.org/standards/DACS/part_I/chapter_1) required elements. 

DACSspace utilizes the ArchivesSpace API to check all **published** resources for DACS compliance and produces a csv containing a list of evaluated resources. If the DACS field is present it's content will be written to the csv, if the field is missing the csv will read "FALSE" for that item.

## Requirements

*   Python (written for and tested on 2.7).
*   ConfigParser
*   Requests module

## Installation

Download [Python](https://www.python.org/downloads/)

If you are using Windows, add Python to your [PATH variable](https://docs.python.org/2/using/windows.html)

Install requirements ([ConfigParser instructions](https://docs.python.org/2/library/configparser.html) /  [Requests instructions](http://docs.python-requests.org/en/master/user/install/))

## Usage

Run `setup.py` to create a configuration file named `local_settings.cfg` which will allow you to connect to your ArchivesSpace instance. You will need:
* BaseURL of your ArchivesSpace instance
* Repository ID for your ArchivesSpace installation
* ArchivesSpace username and password

Your configuration file will look something like this:
```
[ArchivesSpace]
baseURL: #BaseURL of your ArchivesSpace instance
repository: #Repository ID of your ArchivesSpace installation
user: #ArchivesSpace username
password: #ArchivesSpace password for the username used above

[Destinations]
directory: #Directory where you would like to save the csv file
filename: dacs_singlelevel_report.csv
```

Using the command line navigate to the directory containing the DACSspace repository and run `single-level.py` to execute the script.

The script will create a list of evaluated resources in a csv file (default is `dacs_singlelevel_report.csv`).

A sample csv file will look like this:

| title  | resource |extent  | language | repository | creator | scopecontent | accessrestrict
| ---|---| ---|----| ---| --- | --- | ---- |
| #resource title     | #resourceId | #inclusive| #eng | #NameofRepository | #FALSE | #scopecontent| #accessrestrict
| #resource title     | #resourceId | #single | #FALSE | #NameofRepository | #creator | #FALSE| #FALSE

If you are using Microsoft Excel to view the csv file consult the following links to avoid encoding issues: [Excel 2007](https://www.itg.ias.edu/content/how-import-csv-file-uses-utf-8-character-encoding-0), [Excel 2013](https://www.itg.ias.edu/node/985).

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold and Amy Berish

## License

This code is released under the MIT license. See `LICENSE` for further details.