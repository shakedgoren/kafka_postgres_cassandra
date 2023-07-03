import configparser
import json
from time import sleep
from datetime import datetime
from kafka import KafkaProducer
import random
from colorama import Fore

config = configparser.ConfigParser()
config.read('myConfig.ini')
bootstrap_servers = config.get('Kafka', 'bootstrap_servers')
topic = config.get('Kafka', 'topic')
partition = int(config.get('Kafka', 'partition'))
sleepTime = int(config.get('Kafka', 'sleepTime'))
randomMin = int(config.get('Kafka', 'randomMin'))
randomMax = int(config.get('Kafka', 'randomMax'))
reload = int(config.get('Kafka', 'reload'))
successMessage = config.get('Kafka', 'successMessage')
errorMessage = config.get('Kafka', 'errorMessage')

class MyKafkaData:
    def __init__(self, orderId, timeStamp, randomId, message):
        self.orderId:int = orderId
        self.timeStamp:datetime = timeStamp
        self.randomId:int = randomId
        self.message:str = message

def produce_data():
    orderId = 1
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer = lambda v: json.dumps(v).encode('utf-8')
            )
            print(Fore.GREEN + successMessage)
            timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            randomId = random.randint(randomMin,randomMax)
            message = config.get('Kafka', 'message')
            message = message.replace("timestamp",timeStamp)
            key = timeStamp
            fullValue = MyKafkaData(orderId,timeStamp,randomId,message)
            producer.send(
                topic,
                partition=partition,
                key=key.encode("utf-8"),
                value=fullValue.__dict__,
            )
            producer.flush()
            orderId += 1
            sleep(sleepTime)
           
        except:
            print(Fore.RED + errorMessage)
            sleep(reload)

if __name__ == '__main__':
    produce_data()