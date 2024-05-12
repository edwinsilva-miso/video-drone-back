CREATE TABLE processing_task (
    video_id varchar(250) unique,
    create_time timestamp,

    PRIMARY KEY (video_id)
);
