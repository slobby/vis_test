# VIS_tester

## Сontent

- [VIS_tester](#vis_tester)
  - [Сontent](#сontent)
    - [The stucture what you need to know](#the-stucture-what-you-need-to-know)
  - [How to config](#how-to-config)
    - [File config/config[N].py](#file-configconfignpy)
    - [File config/default_description.csv](#file-configdefault_descriptioncsv)
    - [File stations/STATION/description.csv](#file-stationsstationdescriptioncsv)
    - [File stations/STATION/\*\*/test\*.csv](#file-stationsstationtestcsv)
  - [How to use](#how-to-use)
  - [Requirements](#requirements)
      - [Windows](#windows)
      - [Linux](#linux)
  - [CLI command](#cli-command)
  - [See the results](#see-the-results)
    - [Directory output](#directory-output)
  - [See log](#see-log)

### The stucture what you need to know

├──config\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── config.py\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── config1.py\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── default_description.csv.py\
│\
├── stations\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Gorochichi\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── description.csv \
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test2.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── other_test.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Service\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test2.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── other_test.csv\
│\
├── outputs\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── Gorochichi\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1_log.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test2.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── test2_log.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── Service\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test1_log.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── test2.csv\
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── test2_log.csv\

## How to config

### File config/config[N].py

Contain config setting for client and test directory

- SERVER_HOST {str} - Visualisation host IP address

```
SERVER_HOST = 'localhost'/'192.168.1.1'
```

- SERVER_PORT {int|byte} - TCP listen port

```
TCP_PORT = 5555
```

- STATION {str} - Station 'name'. Used for opening proper 'stations/STATION/description.csv' file,\
  read tests cases from folder 'stations/STATION/\*\*' and write in folder 'output/STATION/' report files

```
STATION = "Gorochichi"
```

### File config/default_description.csv

Contains global descriptions for stations model in csv format.

### File stations/STATION/description.csv

Contains local description for station model in csv format.

### File stations/STATION/\*\*/test\*.csv

Contains test cases for station model in csv format.

Files start with prefix 'test' will be automaticaly collected if you don`t use property '-t' (see below)

## How to use

## Requirements

run `pyp install -r requirements.txt`

#### Windows

- install python 3.5 or above
- to run as a console app, in root project directory run
  `run.bat` or `py start.py`

#### Linux

- in root project directory run
  `python3 start.py`

## CLI command

```
Usage: start.py [OPTIONS]

Options:
  -c, --config TEXT     Config file name.
  -t, --test TEXT       Test files name in station folder. Can be multiple.
  -f, --fixture TEXT    Test files executed after every failed test. Can be
                        multiple.
  -r, --repeat INTEGER  Set repeat tests (if they are succsseful).
  -v, --verbose         Show more info.
  --help                Show this message and exit.
```

## See the results

### Directory output

output/STATION/\*/test\*.csv contains just one record passed/failed \
output/STATION/\*/test\*\_log.csv contains test progress messages, failure reasons

## See log

Directory log
