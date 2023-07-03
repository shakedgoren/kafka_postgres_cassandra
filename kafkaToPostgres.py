import configparser
from datetime import datetime
import json
from kafka import KafkaConsumer
import psycopg2
from time import sleep
from colorama import Fore

config = configparser.ConfigParser()
config.read('myConfig.ini')
bootstrap_servers = config.get('Kafka', 'bootstrap_servers')
topic = config.get('Kafka', 'topic')
groupId = config.get('Kafka', 'groupId')
host = config.get('PostGresql', 'host')
port = config.get('PostGresql', 'port')
dbname = config.get('PostGresql', 'dbname')
user = config.get('PostGresql', 'user')
password = config.get('PostGresql', 'password')
table = config.get('PostGresql', 'table')
successMessage = config.get('PostGresql', 'successMessage')
errorMessage = config.get('PostGresql', 'errorMessage')
reload = int(config.get('Kafka', 'reload'))

class MyPostgresqlData:
    def __init__(self, orderId, timeStamp, randomId, message):
        self.orderId:int = orderId
        self.timeStamp:datetime = timeStamp
        self.randomId:int = randomId
        self.message:str = message
        
def toPostgresql():
    postGresConnection = psycopg2.connect(
        host = host,
        port = port,
        dbname = dbname,
        user = user,
        password = password,
    )
    postGresCur = postGresConnection.cursor()
    postGresCur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table} (
            orderId INT,
            timeStamp TIMESTAMP PRIMARY KEY,
            randomId INT,
            message VARCHAR(150)
    );
    """)
    postGresCur.execute(f"SELECT * FROM {table};")
    while True:
        try:
            count = postGresCur.fetchone()[0]
        except:
            count = 0

        if count == 0:
            result = 'earliest'
        else:
            result = 'latest'
        print(Fore.GREEN + successMessage)
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers = bootstrap_servers,
            value_deserializer = lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset = f'{result}',
            group_id = groupId
        )
        consumer.subscribe(topics=[topic])
        try:
            for fullValue in consumer:
                myValue = fullValue.value
                print(myValue)
                orderId = myValue['orderId']
                timeStamp = datetime.strptime(myValue['timeStamp'], "%Y-%m-%d %H:%M:%S")
                randomId = myValue['randomId']
                message = myValue['message']
                myFullValue = MyPostgresqlData(orderId, timeStamp, randomId, message)
                postGresCur.execute(f"SELECT timeStamp FROM {table} WHERE timeStamp = %s", (timeStamp,))
                existing_row = postGresCur.fetchone()
                if existing_row:
                    continue
                postGresCur.execute(
                    f"INSERT INTO {table} (orderId, timeStamp, randomId, message) VALUES (%s, %s, %s, %s)",
                    (myFullValue.orderId,myFullValue.timeStamp,myFullValue.randomId,myFullValue.message)
                )
                postGresConnection.commit()
            postGresConnection.commit()
            postGresCur.close()
            postGresConnection.close()
        except:
            print(Fore.RED + errorMessage)
            sleep(reload)
        
if __name__ == '__main__':
    toPostgresql()

    