# logio

Parse log file as input and export the data to database as output.

## Install

```
pip install logio
```

## Installed Command Utils

- logio

## Usage

```
C:\Workspace\logio>logio --help
Usage: logio [OPTIONS] COMMAND [ARGS]...

  Parse log file as input and export the data to database as output.

Options:
  -c, --config TEXT  Config file path. The config file must in yaml format.
                     [required]

  --help             Show this message and exit.

Commands:
  scan    Try example settings on a test file.
  server  Start log handler server.
  test    Parse the example text and print out parse result.
```

## Settings

- input
  - type: stdin, file, tail
  - ignore-blank-lines: true, false
  - encoding: utf-8, gb18030, ...
  - **for type=file**
  - filename
  - **for type=tail**
  - filename
  - offset-file
  - read-from-end
  - backup-patterns
  - sleep-interval
  - non-blocking
  - blocking
- output
  - type: mysql, stdout, print-not-matched-line
  - buffer-size
  - **for type=mysql**
  - ignore-not-matched-lines
  - keep-failed-lines
  - inserts: list<string, string>
    - key: DEFAULT, some other key
    - sql_template
- parser
  - type: regex, json
  - keeep-not-matched-lines: bool
  - **for type=regex**
  - use-default-rules
  - transforms
  - rules
  - matches: list<string, string>
    - matched_name
    - regex

## Example config

```
input:
  type: tail
  filename: tests\nginx.access.log
parser:
  type: regex
  matches:
    simple: "{SIMPLE_NGINX_ACCESS}"
  transforms:
    - field: time_local
      type: strftime
      strptime: "%d/%b/%Y:%H:%M:%S %z"
    - field: request_time
      type: str2number
    - field: request_time
      type: formula
      formula: "{request_time} * 1000000"
    - field: request_time
      type: int
output:
  type: mysql
  mysql:
    host: 127.0.0.1
    port: 3306
    user: root
    password: password
    database: database
  inserts:
    simple:
      sql: insert into table_name (add_time, path, response_time) values (%s, %s, %s)
      fields:
        - time_local
        - request_path
        - request_time
```

## Releases

### v0.1.19 2022/01/18

- Add sympy in requirements.txt.
- Remove mysqlclient from requirements.txt.
- Fix license file missing problem.

### v0.1.18 2021/02/22

- Set default buffer-size to 10.
- Add log in loop.
- Use fastutils.logutils.setup.

### V0.1.13 2021/02/18

- Add Nginx Access Log Rules.
- Add LogFilter subsystem.
- Add transforms support in LogParser.

### v0.1.10 2020/10/10

- Add json parser.

### v0.1.9 2020/09/10

- Change package's home url.

### v0.1.8 2020/09/09

- Translate help informations to english.
- Add License.
- Add LogToStdout.

### v0.1.7

- Some bad old release, ignore them...

