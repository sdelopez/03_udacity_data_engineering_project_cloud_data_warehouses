import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    print('Extract data from S3 to Staging Tables')
    print('Extracting full Song Data can take more than one hour ! Please be patient ...')
    load_staging_tables(cur, conn)
    print('Transform & Load data to Facts and Dimensions Tables')
    insert_tables(cur, conn)
    print('Sparkify ETL process completed !')

    conn.close()


if __name__ == "__main__":
    main()