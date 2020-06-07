[UDACITY DATA ENGINEERING NANODEGREE](https://classroom.udacity.com/nanodegrees)

Project: Cloud Data Warehouses
----

# **Introduction**

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

# **Project Description**
In this project, you'll apply what you've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, you will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

# Project Datasets
You'll be working with two datasets that reside in S3. Here are the S3 links for each:

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data
- Log data json path: s3://udacity-dend/log_json_path.json

# **Project Files**

- **requirements.txt** PIP install requirements to install necessary python packages

- **sparkigy_redshift_dwh_etl.ipynb** Jupyter notebook to use for managing AWS Redshift cluster
    - to read and process files from song_data and log_data in S3 buckets
    - Manage Redshift cluster using code (Infrastructure as Code - IaC)  
    - Run python scripts to create tables and run ETL process
    - check that data were correctly processed with ETL scripte with SQL queries
    - delete Redshift cluster at the end of the process to avoid AWS cost

- **sql_queries.py** containg all sql queries :  
    - to drop, create staging, fact and dimension tables  
    - copy S3 data to staging tables  
    - transform and load data from staging tables to fact and dimension table sparkify datawarehouse

- **create_tables.py** script to drop and create tables in sparkify datawarehouse. This script must be ran to reset the database in Redshift cluster
- **etl.py**  script to run ETL process
    - Extract data from song_data and log_data in S3 bucket to staging tables
    - Transform data in staging table and Load them to Fact and Dimension tables in sparkify datawarehouse  

# ETL logic

## Schema for staging tables

Song and log event data in S3 buckets will be extracted into 2 staging tables :
- **staging_events** - events in the app ie artist, auth, firstName, gender, itemInSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, userId
- **staging_songs** - songs data ie song_id, num_songs, title, artist_name, artist_latitude, year, duration, artist_id, artist_longitude, artist_location  

## Schema for Song Play Analysis
We will create a star schema optimized for queries on song play analysis. This includes the following tables. Using the song and event datasets in staging tables, will be transformed and loaded into the fact and diemnsions tables using SQL queries.  

**Fact Table**
- **fact_songplay** - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent  

**Dimension Tables**
- **dim_user** - users in the app
user_id, first_name, last_name, gender, level -> user_id is used as a distkey to minimize shuffling between nodes
- **dim_song** - songs in music database
song_id, title, artist_id, year, duration -> artist_id is used as a distkey to minimize shuffling between nodes
- **dim_artist** - artists in music database
artist_id, name, location, lattitude, longitude -> artist_id is used as a distkey to minimize shuffling between nodes
- **dim_time** - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday -> start_time is used as a distkey to minimize shuffling between nodes

# Steps to implement ETL in AWS Redshift Datawarehouse

We followed tgese steps to implement the ETL process

1. Create Table Schemas
- Design schemas for your fact and dimension tables
- Write a SQL CREATE statement for each of these tables in sql_queries.py
- Complete the logic in create_tables.py to connect to the database and create these tables
- Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
- Launch a redshift cluster and create an IAM role that has read access to S3.
- Add redshift database and IAM role info to dwh.cfg.
- Test by running create_tables.py and checking the table schemas in your redshift database. You can use Query Editor in the AWS Redshift console for this.
2. Build ETL Pipeline
- Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
- Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
- Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
- Delete your redshift cluster when finished.

# Running the ETL code

The starting point is running all the ETL steps from the Jupyter notebook [sparkigy_redshift_dwh_etl.ipynb](./sparkigy_redshift_dwh_etl.ipynb)

0. Import Python packages
1. Load DWH Params from a file
2. Create clients for EC2, S3, IAM, and Redshift
3. Explore Sparkify data sources on S3
4. Configure AWS Redshit Cluster - Infrastructure as Code
    1. Create IAM ROLE
    2. Create Redshift Cluster
        1. Check the cluster to see its status
        2. Set the cluster endpoint and role ARN -> set CLUSTER endpoint and ARN in dwh.cfg file
    3. Open an incoming TCP port to access the cluster ednpoint
    4. Check connection to the cluster
5. Sparkify ETL Process
    1. Create Staging, Facts and Dimension Tables in Redshift DWH. Run in a console 
        ```python
        python create_tables.py
        ```

    2. Run ETL pipelines to Extract raw data to staging tables, Transform and Load data to Facts & Dimension tables. Run in a console 
        ```python
        python etl.py
        ```
        **Be aware that the copy step from S3 to staging for songs data can be very long (> 1 hour) for the full songs dataset**  
        For checking and development purpose, we can ran the ETL on a subset of the songs data.  
        To do so change SONG_DATA to SONG_DATA_SUBSET in sql query in sql_queries.py file
        ```SQL
        staging_songs_copy = ("""
                        COPY staging_songs FROM {}
                        CREDENTIALS 'aws_iam_role={}'
                        COMPUPDATE OFF region 'us-west-2'
                        FORMAT AS JSON 'auto' 
                        TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL;
                    """).format(SONG_DATA_SUBSET, IAM_ROLE)
        ```

6. Check that DWH tables were populated correctly by ETL process
    1. Check Staging Tables
    2. Check Fact and Dimension Tables
7. Clean AWS Redshift Cluster & IAM role
    1. Clean Redshift Cluster
    2. Clean AWS IAM role/policy
