# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

class ProcoreContractorsPipeline:
    def process_item(self, item, spider):
        return item

class SaveToPostgresDatabase:
    def __init__(self):
        hostname = os.getenv("DATABASE_HOST")
        username = os.getenv("DATABASE_USERNAME")
        password = os.getenv("DATABASE_PASSWORD")
        database_name = os.getenv("DATABASE_NAME")
        port = os.getenv("DATABASE_PORT")

        print(hostname, username, password, database_name, port)

        # Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database_name, port=port)
        
        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        
        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS contractors(
            company_id SERIAL PRIMARY KEY, 
            company_name VARCHAR(255) NOT NULL,
            company_website TEXT NOT NULL,
            company_type VARCHAR(255) NOT NULL,
            company_province VARCHAR(255) NOT NULL
        )
        """)

        self.connection.commit()

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute(""" insert into contractors (company_name, company_website, company_type, company_province) values (%s, %s, %s, %s)""", (
            item["company_name"],
            item["website"],
            item["company_type"],
            item["province"]
        ))

        ## Execute insert of data into database
        self.connection.commit()
        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()