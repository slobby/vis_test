# VIS_tester

## Сontent

- [VIS_tester](#vis_tester)
  - [Сontent](#сontent)
    - [The stucture what you need to know](#the-stucture-what-you-need-to-know)
  - [How to config](#how-to-config)
    - [File config/config[N].py](#file-configconfignpy)
    - [File config/default_description.csv](#file-configdefault_descriptioncsv)
      - [1-st. [Visualisation]](#1-st-visualisation)
      - [2-nd. [Tester]](#2-nd-tester)
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
  - [Protocol description](#protocol-description)
  - [Описание строк директив файлов для тестирования состояния обьектов приложений Visualisation и Tester](#описание-строк-директив-файлов-для-тестирования-состояния-обьектов-приложений-visualisation-и-tester)
    - [[Секция для описания общих директив]](#секция-для-описания-общих-директив)
      - [I. Уснуть на время](#i-уснуть-на-время)
    - [[Секция для описания директив для Visualisation]](#секция-для-описания-директив-для-visualisation)
      - [I. Получить состояние](#i-получить-состояние)
      - [II. Отправить команду](#ii-отправить-команду)
    - [[Секция для описания директив для Tester]](#секция-для-описания-директив-для-tester)
      - [I. Получить состояние](#i-получить-состояние-1)
      - [II. Отправить команду](#ii-отправить-команду-1)
      - [III. Установить импульс](#iii-установить-импульс)

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

- CLIENT_ID Type[str] - Default visualisation ID

```
CLIENT_ID = 'ДНЦ'
```

Contain config setting for client and test directory

- CLIENT_HOST Type[str] - Default client host IP address

```
CLIENT_HOST = 'localhost'
```

- CLIENT_PORT Type[int|bytes] - Default client host TCP port

```
CLIENT_PORT = 5555
```

- CLIENTS Type[dict[str: tuple[str, int|byte]]] - Dictionary of clients

```
CLIENTS = {
    CLIENT_ID: (CLIENT_HOST, CLIENT_PORT),
    'ТЕСТ': ('localhost', 5556)
    # 'ШН': ('localhost',5555),
}
```

Use CLIENT_ID/'ТЕСТ'/.. name in your test files to send requests to apropriate client

- STATION Type[str] - Station 'name'. Used for opening proper 'stations/STATION/description.csv' file,\
  read tests cases from folder 'stations/STATION/\*\*' and write in folder 'output/STATION/' report files

```
STATION = "Gorochichi"
```

### File config/default_description.csv

Contains global descriptions for stations model in csv format.

Consists from two parts.

#### 1-st. [Visualisation]

alias;id_object \
Type[str];Type[int] - id`s for objects name

alias;id_color \
Type[int];Type[str] - aliases for color id`s

id_object;state;layer_number;permanent_id_color,blink_id_color \
Type[int];Type[str];Type[int];Type[str],Type[str] - describes colors in each layer for particular state

#### 2-nd. [Tester]

state;impulse_value \
{str};{int} - id`s for impulses state

### File stations/STATION/description.csv

Contains local description for station model and tester in csv format.

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
  -s, --success TEXT    Test files executed after every successful test. Can
                        be multiple.
  -t, --test TEXT       Test file/folder name in station folder. Can be
                        multiple.
  -f, --fixture TEXT    Test files executed after every failed test. Can be
                        multiple.
  -r, --repeat INTEGER  Set repeat tests (if they are succsseful).
  -v, --verbose         Show more info.
  --help                Show this message and exit.
```

| Option | Description                                                             | Example                         |
| ------ | ----------------------------------------------------------------------- | ------------------------------- |
| -c     | The name of config file in folder config                                | -c config2                      |
| -t     | Test file/folder name in station folder. Can be multiple                | -t 1_switches                   |
|        | If you set folder. Only files starts with 'test' prefix will be handled | -t 2_routes\N1                  |
|        | You can set any file name.                                              | -t 2_routes\N1\extra_ttest      |
| -f     | Test files executed after every failed test. Can be multiple            | -f fixtures\reset\reset_bottoms |
| -s     | Test files executed after every succesful test. Can be multiple         | -s success\send_signals         |
| -r     | Set repeat tests (if they are succsseful)                               | -r 2                            |
| -v     | Show info about each action                                             | -v                              |

## See the results

### Directory output

output/STATION/\*/test\*.csv contains just one record passed/failed \
output/STATION/\*/test\*\_log.csv contains test progress messages, failure reasons

## See log

Directory log

## Protocol description

## Описание строк директив файлов для тестирования состояния обьектов приложений Visualisation и Tester

### [Секция для описания общих директив]

#### I. Уснуть на время

1\
waiting_time

| pos | Param name     | Param type | Required     | Description                                    | Example |
| --- | -------------- | ---------- | ------------ | ---------------------------------------------- | ------- |
| 1   | 'waiting_time' | Type[int]  | обязательный | время в секундах на которое программа засыпает | 20      |

### [Секция для описания директив для Visualisation]

#### I. Получить состояние

vis::client_id;station_id;station_sub_id;object_type_name;object_name;object_state[?[elapsed_time]]

| pos | Param name         | Param type | Required       | Description                                                                                              | Example   |
| --- | ------------------ | ---------- | -------------- | -------------------------------------------------------------------------------------------------------- | --------- |
| 1   | 'vis'              | Type[str]  | обязательный   | маркер, строка для Visualisation                                                                         | vis       |
| 2   | '::'               | Type[str]  | обязательный   | разделитель между типом приложения и остальными параметрами                                              | ::        |
| 3   | 'client_id'        | Type[str]  | обязательный   | имя TCP клиента куда будет отправлен запрос из данной строки                                             | ШНД       |
| 4   | ';'                | Type[str]  | обязательный   | разделитель параметров                                                                                   | ;         |
| 5   | 'station_id'       | Type[int]  | обязательный   | код станции                                                                                              | 7600056   |
| 6   | 'station_sub_id'   | Type[int]  | обязательный   | код графической модели станции                                                                           | 2         |
| 7   | 'object_type_name' | Type[str]  | обязательный   | имя типа обьекта состояние которого получаем                                                             | вход      |
| 8   | 'object_name'      | Type[str]  | обязательный   | имя обьекта состояние которого получаем                                                                  | Н         |
| 9   | 'object_state'     | Type[str]  | обязательный   | имя состояния которое хотим получить в ответе                                                            | Н         |
| 10  | '?'                | Type[str]  | необязательный | активация режима 'попытка ожидания желаемого состояния object_state в течении времени 'elapsed_time'     | [,?, ?24] |
| 11  | 'elapsed_time'     | Type[int]  | необязательный | время на которое включается режим 'попытка ожидания желаемого состояния в течении времени 'elapsed_time' | 15        |

По умолчанию:

1. Если не указан 'elapsed_time' активация режима будет в течении 60 секунд

из полученной директивы получаем сообщение для отправки клиенту 'client_id'

GET:station_id:station_sub_id:object_type_id:object_name

| pos | Param name       | Param type | Required     | Description                                                             | Example |
| --- | ---------------- | ---------- | ------------ | ----------------------------------------------------------------------- | ------- |
| 1   | 'GET'            | Type[str]  | обязательный | маркер, запрос на получение состояния                                   | GET     |
| 2   | 'station_id'     | Type[int]  | обязательный | код станции                                                             | 7600056 |
| 3   | 'station_sub_id' | Type[int]  | обязательный | код графической модели станции                                          | 2       |
| 4   | 'object_type_id' | Type[int]  | обязательный | код типа обьекта состояние которого получаем(берется из файла настроек) | 3       |
| 5   | 'object_name'    | Type[str]  | обязательный | имя обьекта состояние которого получаем                                 | Н       |

Типы ответа на запрос типа GET:\

**1.**

ERR_FORMAT

| pos | Param name   | Param type | Required     | Description                                | Example    |
| --- | ------------ | ---------- | ------------ | ------------------------------------------ | ---------- |
| 1   | 'ERR_FORMAT' | Type[str]  | обязательный | неправильный запрос(/нет такого кода типа) | ERR_FORMAT |

**2.**

station_id:station_sub_id:object_type_id:object_name:NO

| pos | Param name       | Param type | Required     | Description                                                             | Example |
| --- | ---------------- | ---------- | ------------ | ----------------------------------------------------------------------- | ------- |
| 1   | 'station_id'     | Type[int]  | обязательный | код станции                                                             | 7600056 |
| 2   | 'station_sub_id' | Type[int]  | обязательный | код графической модели станции                                          | 2       |
| 3   | 'object_type_id' | Type[int]  | обязательный | код типа обьекта состояние которого получаем(берется из файла настроек) | 3       |
| 4   | 'object_name'    | Type[str]  | обязательный | имя обьекта состояние которого получаем                                 | Н       |
| 5   | 'NO'             | Type[str]  | обязательный | неправильный запрос(/нет такого имя обьекта)                            | NO      |

**3.**

station_id:station_sub_id:object_type_id:object_name:[layer_id, color_active_phase_id, [color_pasive_phase_id]:]

| pos | Param name              | Param type | Required       | Description                                                             | Example |
| --- | ----------------------- | ---------- | -------------- | ----------------------------------------------------------------------- | ------- |
| 1   | 'station_id'            | Type[int]  | обязательный   | код станции                                                             | 7600056 |
| 2   | 'station_sub_id'        | Type[int]  | обязательный   | код графической модели станции                                          | 2       |
| 3   | 'object_type_id'        | Type[int]  | обязательный   | код типа обьекта состояние которого получаем(берется из файла настроек) | 3       |
| 4   | 'object_name'           | Type[str]  | обязательный   | имя обьекта состояние которого получаем                                 | Н       |
| 5   | 'layer_id'              | Type[int]  | обязательный   | код слоя                                                                | 1       |
| 6   | 'color_active_phase_id' | Type[int]  | обязательный   | цвет активной фазы мигания/цвет примитива этого слоя                    | 22      |
| 7   | 'color_pasive_phase_id' | Type[int]  | необязательный | цвет пассивной фазы мигания/отсутствует если нет мигания                | 256     |

#### II. Отправить команду

vis::client_id;station_id;object_type_name;object_name;command_name[:command_type]

| pos | Param name         | Param type | Required       | Description                                                   | Example |
| --- | ------------------ | ---------- | -------------- | ------------------------------------------------------------- | ------- |
| 1   | 'vis'              | Type[str]  | обязательный   | маркер, строка для Visualisation                              | vis     |
| 2   | '::'               | Type[str]  | обязательный   | разделитель между типом приложения и остальными параметрами   | ::      |
| 3   | ';'                | Type[str]  | обязательный   | разделитель параметров                                        | ;       |
| 4   | 'client_id'        | Type[str]  | обязательный   | имя tcp клиента куда буддет отправлен запрос из данной строки | ДНЦ     |
| 5   | 'station_id'       | Type[int]  | обязательный   | код станции                                                   | 7600056 |
| 6   | 'object_type_name' | Type[str]  | обязательный   | имя типа обьекта команды                                      | вход    |
| 7   | 'object_name'      | Type[str]  | обязательный   | имя обьекта команды                                           | Н       |
| 8   | 'command_name'     | Type[str]  | обязательный   | имя команды                                                   | Н       |
| 9   | :'command_type'    | Type[int]  | необязательный | тип команды: 0-обычная, 1-предварительная, 2-ответственная    | :0      |

из полученной директивы получаем сообщение для отправки клиенту 'client_id'

CMD:station_id:object_type_id:object_name:command_name:command_type

| pos | Param name       | Param type | Required     | Description                                                             | Example |
| --- | ---------------- | ---------- | ------------ | ----------------------------------------------------------------------- | ------- |
| 1   | 'CMD'            | Type[str]  | обязательный | маркер, запрос на выполнение команды                                    | CMD     |
| 2   | 'station_id'     | Type[int]  | обязательный | код станции                                                             | 7600056 |
| 3   | 'object_type_id' | Type[int]  | обязательный | код типа обьекта состояние которого получаем(берется из файла настроек) | 3       |
| 4   | 'object_name'    | Type[str]  | обязательный | имя обьекта состояние которого получаем                                 | Н       |
| 5   | 'command_name'   | Type[str]  | обязательный | имя команды                                                             | Н       |
| 6   | 'command_type'   | Type[int]  | обязательный | тип команды: 0-обычная, 1-предварительная, 2-ответственная              | 0       |

Типы ответа на запрос типа CMD:

**1.**

ERR_FORMAT

| pos | Param name   | Param type | Required     | Description                                 | Example    |
| --- | ------------ | ---------- | ------------ | ------------------------------------------- | ---------- |
| 1   | 'ERR_FORMAT' | Type[str]  | обязательный | неправильный запрос(/нет такого кода типа). | ERR_FORMAT |

**2.**

CMD:station_id:object_type_id:object_name:command_name:confirmation

| pos | Param name         | Param type | Required     | Description                                               | Example |
| --- | ------------------ | ---------- | ------------ | --------------------------------------------------------- | ------- |
| 1   | 'CMD'              | Type[str]  | обязательный | маркер, запрос на выполнение команды                      | CMD     |
| 5   | 'station_id'       | Type[int]  | обязательный | код станции                                               | 7600056 |
| 6   | 'object_type_name' | Type[str]  | обязательный | имя типа обьекта команды                                  | вход    |
| 7   | 'object_name'      | Type[str]  | обязательный | имя обьекта команды                                       | Н       |
| 8   | 'command_name'     | Type[str]  | обязательный | имя команды                                               | Н       |
| 5   | 'confirmation'     | Type[str]  | обязательный | состояние отправки команды OK-отправлена, NO-неотправлена | NO      |

### [Секция для описания директив для Tester]

#### I. Получить состояние

tester::client_id;table_id;impulse_name;impulse_state[?[elapsed_time]]

| pos | Param name      | Param type | Required       | Description                                                                                              | Example                                |
| --- | --------------- | ---------- | -------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 1   | 'tester'        | Type[str]  | обязательный   | маркер, строка для Tester                                                                                | test                                   |
| 2   | '::'            | Type[str]  | обязательный   | разделитель между типом приложения и остальными параметрами                                              | ::                                     |
| 3   | 'client_id'     | Type[str]  | обязательный   | имя TCP клиента куда буддет отправлен запрос из данной строки                                            | ШНД                                    |
| 4   | ';'             | Type[str]  | обязательный   | разделитель параметров                                                                                   | ;                                      |
| 5   | 'table_id'      | Type[int]  | обязательный   | код станции                                                                                              | 7600056                                |
| 6   | 'impulse_name'  | Type[str]  | обязательный   | имя импульса состояние которого получаем                                                                 | Н                                      |
| 7   | 'impulse_state' | Type[str]  | обязательный   | имя состояния код которого хотим получить в ответе                                                       | [активный,пассивный,нет данных,ошибка] |
| 8   | '?'             | Type[str]  | необязательный | активация режима 'попытка ожидания желаемого состояния object_state в течении времени 'elapsed_time'     | [,?, ?24]                              |
| 9   | 'elapsed_time'  | Type[int]  | необязательный | время на которое включается режим 'попытка ожидания желаемого состояния в течении времени 'elapsed_time' | 15                                     |

По умолчанию:

1. Если не указан 'elapsed_time' активация режима будет в течении 60 секунд

из полученной директивы получаем сообщение для отправки клиенту 'client_id'

GET:table_id:impulse_name

| pos | Param name     | Param type | Required     | Description                           | Example |
| --- | -------------- | ---------- | ------------ | ------------------------------------- | ------- |
| 1   | 'GET'          | Type[str]  | обязательный | маркер, запрос на получение состояния | GET     |
| 2   | 'table_id'     | Type[int]  | обязательный | код таблицы                           | 7600056 |
| 3   | 'impulse_name' | Type[str]  | обязательный | импульса состояние которого получаем  | Н       |

Типы ответа на запрос типа GET:
**1.**

table_id:impulse_state:NO

| pos | Param name     | Param type | Required     | Description                                   | Example |
| --- | -------------- | ---------- | ------------ | --------------------------------------------- | ------- |
| 1   | 'table_id'     | Type[int]  | обязательный | код станции                                   | 3       |
| 2   | 'impulse_name' | Type[str]  | обязательный | имя импульса состояние которого получаем      | Н       |
| 3   | 'NO'           | Type[str]  | обязательный | либо таблицы нет, либо импульса в таблице нет | NO      |

**2.**

table_id:impulse_state:state

| pos | Param name     | Param type | Required     | Description                                     | Example |
| --- | -------------- | ---------- | ------------ | ----------------------------------------------- | ------- |
| 1   | 'table_id'     | Type[int]  | обязательный | код станции                                     | 3       |
| 2   | 'impulse_name' | Type[str]  | обязательный | имя импульса состояние которого получаем        | Н       |
| 3   | 'state'        | Type[str]  | обязательный | 0-ошибка, 1-нет данных, 2-пассивный, 3-активный | 3       |

#### II. Отправить команду

test::client_id;table_id;command_name[:command_type]

| pos | Param name      | Param type | Required     | Description                                                   | Example |
| --- | --------------- | ---------- | ------------ | ------------------------------------------------------------- | ------- |
| 1   | 'test'          | Type[str]  | обязательный | маркер, строка для Tester                                     | test    |
| 2   | '::'            | Type[str]  | обязательный | разделитель между типом приложения и остальными параметрами   | ::      |
| 3   | 'client_id'     | Type[str]  | обязательный | имя TCP клиента куда буддет отправлен запрос из данной строки | ШНД     |
| 4   | ';'             | Type[str]  | обязательный | разделитель параметров                                        | ;       |
| 5   | 'table_id'      | Type[int]  | обязательный | код станции                                                   | 7600056 |
| 6   | 'command_name'  | Type[str]  | обязательный | имя команды импульса ТУ                                       | Н       |
| 7   | :'command_type' | Type[int]  | обязательный | тип команды: 0-пассивная, 1-активная                          | :0      |

из полученной директивы получаем сообщение для отправки клиенту 'TCP_id'

CMD:table_id:command_name:command_type

| pos | Param name     | Param type | Required     | Description                          | Example |
| --- | -------------- | ---------- | ------------ | ------------------------------------ | ------- |
| 1   | 'CMD'          | Type[str]  | обязательный | маркер, запрос на выполнение команды | CMD     |
| 2   | 'table_id'     | Type[int]  | обязательный | код станции                          | 7600056 |
| 3   | 'command_name' | Type[str]  | обязательный | имя команды импульса ТУ              | Н       |
| 4   | 'command_type' | Type[int]  | обязательный | тип команды: 0-пассивная, 1-активная | 0       |

Типы ответа на запрос типа CMD:

CMD:table_id:command_name:confirmation

| pos | Param name     | Param type | Required     | Description                                               | Example |
| --- | -------------- | ---------- | ------------ | --------------------------------------------------------- | ------- |
| 1   | 'CMD'          | Type[str]  | обязательный | маркер, запрос на выполнение команды                      | CMD     |
| 2   | 'table_id'     | Type[int]  | обязательный | код станции                                               | 7600056 |
| 3   | 'command_name' | Type[str]  | обязательный | имя команды импульса ТУ                                   | Н       |
| 4   | 'confirmation' | Type[str]  | обязательный | состояние отправки команды OK-отправлена, NO-неотправлена | NO      |

#### III. Установить импульс

test::client_id;table_id;@impulse_name[:impulse_type]

| pos | Param name      | Param type | Required       | Description                                                    | Example |
| --- | --------------- | ---------- | -------------- | -------------------------------------------------------------- | ------- |
| 1   | 'test'          | Type[str]  | обязательный   | маркер, строка для Tester                                      | test    |
| 2   | ':'             | Type[str]  | обязательный   | разделитель между типом приложения и остальными параметрами    | :       |
| 3   | 'client_id'     | Type[str]  | необязательный | имя TCP клиента куда буддет отправлен запрос из данной строки  | ШНД     |
| 4   | ';'             | Type[str]  | обязательный   | разделитель параметров                                         | ;       |
| 5   | 'table_id'      | Type[int]  | обязательный   | код станции                                                    | 7600056 |
| 6   | '@'             | Type[str]  | обязательный   | маркер, того что отправляем команду на установку импульса ТС   | @       |
| 7   | 'impulse_name'  | Type[str]  | обязательный   | имя импульса состояние которого устанавливаем                  | Н       |
| 8   | :'impulse_type' | Type[int]  | обязательный   | тип состояния: 0-ошибка, 1-нет данных, 2-пассивный, 3-активный | :0      |

из полученной директивы получаем сообщение для отправки клиенту 'TCP_id'

CMD:table_id:@impulse_name:impulse_type

| pos | Param name     | Param type | Required     | Description                                                    | Example |
| --- | -------------- | ---------- | ------------ | -------------------------------------------------------------- | ------- |
| 1   | 'CMD'          | Type[str]  | обязательный | маркер, запрос на выполнение команды                           | CMD     |
| 2   | 'table_id'     | Type[int]  | обязательный | код станции                                                    | 7600056 |
| 3   | 'impulse_name' | Type[str]  | обязательный | имя импульса состояние которого устанавливаем                  | Н       |
| 4   | 'impulse_type' | Type[int]  | обязательный | тип состояния: 0-ошибка, 1-нет данных, 2-пассивный, 3-активный | 0       |

Типы ответа на запрос типа CMD:

CMD:table_id:impulse_type:confirmation

| pos | Param name     | Param type | Required     | Description                                                                       | Example |
| --- | -------------- | ---------- | ------------ | --------------------------------------------------------------------------------- | ------- |
| 1   | 'CMD'          | Type[str]  | обязательный | маркер, запрос на выполнение команды                                              | CMD     |
| 2   | 'table_id'     | Type[int]  | обязательный | код станции                                                                       | 7600056 |
| 3   | 'impulse_name' | Type[str]  | обязательный | имя импульса состояние которого устанавливаем                                     | Н       |
| 4   | 'confirmation' | Type[str]  | обязательный | состояние установки импульса OK-установлен, NO-неустановлен в требуемое состояние | NO      |
