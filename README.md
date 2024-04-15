# Video Drone Service

## Description

The Video Drone Service is a component based-on an REST API that manages all processes regarding Video Drone Processing,
Rating and Drone Community (Pilots and Fans).

# Executing the project

## docker compose up

To bring up the application and the database you will run the command:
```shell
docker compose -f docker-compose.yml -p video-drone-back up -d app
```

This will create two docker containers, one called `app`, other `database`. it will take some
time for `app` to be available since it will wait until `database` is in healthy status.

## DB Scripts

After the previous step, you will have to execute some scripts into the PG database for it to be
loaded with some information.

You can use any database GUI of your preference. Use this BD connection:

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


### Postman Documentacion

https://documenter.getpostman.com/view/30729620/2sA3Bj7DWd
