# Video Drone Service

## Description

The Video Drone Service is a component based-on an REST API that manages all processes regarding Video Drone Processing,
Rating and Drone Community (Pilots and Fans).

## Installation

### DB Scripts

In order to configure the database, is required to create a new Postgresql instance via Docker Compose.

```shell
$ cd ~/location/video-drone-back
```

Then, execute the docker-compose command when Docker service is up:

```shell
$ docker-compose up -d postgres
```

After that, you can use any database GUI of your preference. Use this BD connection:

| Property | Value            |
|----------|------------------|
| DB_HOST  | `localhost:5432` |
| DB_USER  | `postgres`       |
| DB_PASS  | `postgres`       |
| DATABASE | `video-drone`    |

#### Execution of DB scripts

In the directory /script of the root application, are the scripts to restore the database:

- [01_ddl_video_drone_db_tables.sql](scripts%2F01_ddl_video_drone_db_tables.sql)
- [02_dml_roles_202404122015.sql](scripts%2F02_dml_roles_202404122015.sql)
- [03_dml_videos_202404122015.sql](scripts%2F03_dml_videos_202404122015.sql)

The scripts are ordered by execution, so is required to run them according to this order.


### Queue Messages

This section is currently unavailable

## Project setup

After the database installation, is required to set up the project. You must be located in the project root:

```shell
$ cd ~/location/video-drone-back
```

### Virtual Env

As the project is writen on python, is required to install a new Virtual Environment. For that purpose, we must execute the command:

```shell
$ python -m virtualenv venv
```

After that, you may activate it:

```shell
$ source venv/bin/activate
```
On Windows, the activate command will be:

```shell
$ .\venv\Scripts\activate
```

### Install dependencies

After the creation of the virtual environment, you may install the requirements for the project.

The following commands are necessary for the installation:

```shell
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
```

## Run project

After that, the project must execute with the command:

```shell
$ python main.py
```

The output is pretty similar to the following. That means the server is up:

```
 * Serving Flask app 'src'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 726-021-831
```
### Postman Documentacion

https://documenter.getpostman.com/view/30729620/2sA3Bj7DWd
