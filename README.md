# DACSspace

A simple Python script to evaluate your ArchivesSpace instance for DACS [single-level minimum](http://www2.archivists.org/standards/DACS/part_I/chapter_1) required elements. 

## Requirements

*   Python (written for and tested on 2.7).
*   ConfigParser
*   Requests module

## Installation

Download [Python](https://www.python.org/downloads/)

Add Python to your [PATH variable](https://docs.python.org/2/using/windows.html)

Install requirements (instructions on installing the Requests module can be found [here](http://docs.python-requests.org/en/master/user/install/))

## Usage

Run `setup.py` to create a configuration file named `local_settings.cfg` which will allow you to connect to your ArchivesSpace instance.

Using the command line navigate to the directory containing the DACSspace repository and run `single-level.py` to execute the script.

The script will create a list of evaluated resources in a csv file (default is `dacsreport.csv`).

If you are using Microsoft Excel to view the csv file consult the following links to avoid encoding issues: [Excel 2007](https://www.itg.ias.edu/content/how-import-csv-file-uses-utf-8-character-encoding-0), [Excel 2013](https://www.itg.ias.edu/node/985).

## Contributing

Pull requests accepted!

## Authors

Hillel Arnold and Amy Berish

## License

This code is released under the MIT license. See `LICENSE` for further details.