# VIS_tester

## How to config

### File config/config.py

- SERVER_HOST {str} - Visualisation host IP address

```
SERVER_HOST = 'localhost'/'192.168.1.1'
```

- SERVER_PORT {int|byte} - TCP listen port

```
TCP_PORT = 5555
```

- STATION {str} - Station 'name'. Used for opening proper 'proper stations/STATION/description.csv' file,\
  read tests cases from folder 'stations' and write in folder 'output/STATION/' report files

```
STATION = "Gorochichi"
```

### File config/default_description.csv

Contains global descriptions for stations model in csv format.

### File stations/STATION/description.csv

Contains local description for station model in csv format.

### File stations/STATION/\*/test\*.csv

Contains test cases for station model in csv format.

## How to use

## Requirements

run `pyp install -r requirements.txt`

#### Windows

- install python 3.5 or above
- to run as a console app, in root project directory run
  `run.bat`

#### Linux

- in root project directory run
  `python3 start.py`

## See the results

### Directory output

output/STATION/\*/test\*.csv contains just one record passed/failed \
output/STATION/\*/test\*\_log.csv contains test progress messages, failure reasons

## See log

Directory log and stdout
