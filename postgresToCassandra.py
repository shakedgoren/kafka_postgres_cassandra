import psycopg2
from cassandra.cluster import Cluster
import configparser
from time import sleep
from datetime import datetime
import json
from colorama import Fore

config = configparser.ConfigParser()
config.read('myConfig.ini')

postg_host = config.get('PostGresql', 'host')
postg_port = config.get('PostGresql', 'port')
postg_dbname = config.get('PostGresql', 'dbname')
postg_user = config.get('PostGresql', 'user')
postg_password = config.get('PostGresql', 'password')
postg_table = config.get('PostGresql', 'table')
errorMessagePost = config.get('PostGresql', 'errorMessage')

cassandra_host = config.get('Cassandra', 'host')
cassandra_port = config.get('Cassandra', 'port')
cassandra_keyspace = config.get('Cassandra', 'keyspace')
cassandra_table = config.get('Cassandra', 'table')
sleepTime = int(config.get('Cassandra', 'sleepTime'))
myJsonFile = config.get('Cassandra', 'myJsonFile')
successMessage = config.get('Cassandra', 'successMessage')
errorMessageCass = config.get('Cassandra', 'errorMessage')
reload = int(config.get('Cassandra', 'reload'))

class MyCassandraData:
    def __init__(self, timeStamp, message):
        self.timeStamp:datetime = timeStamp
        self.message:str = message

def getDataFromPostgresql():
    try:
        with open(myJsonFile, 'r') as file:
            timeStamp = json.load(file)
            try:
                timeStamp = list(timeStamp.keys())[0]
            except:
                pass
        postGresConnection = psycopg2.connect(
            host=postg_host,
            port=postg_port,
            database=postg_dbname,
            user=postg_user,
            password=postg_password
        )
        postGresCur = postGresConnection.cursor()
        if timeStamp == {} :
            postGresCur.execute(f"SELECT timeStamp,message FROM {postg_table};")
        else :
            postGresCur.execute(f"SELECT timeStamp,message FROM {postg_table} WHERE timeStamp > %s", (timeStamp,))
        data = postGresCur.fetchall()
        postGresCur.close()
        postGresConnection.close()
        return data
    except:
        print(Fore.RED + errorMessagePost)
        sleep(reload)

def sendDataToCassandra():
    while True:
        try:
            cass_cluster = Cluster([cassandra_host], port=cassandra_port)
            cass_session = cass_cluster.connect()
            cass_session.execute(f"USE {cassandra_keyspace}")
            cass_session.execute(f"""
                CREATE TABLE IF NOT EXISTS {cassandra_table} (
                    timeStamp TIMESTAMP,
                    message TEXT,
                    PRIMARY KEY(timeStamp)
            );
            """)
            data = getDataFromPostgresql()
            for row in data:
                lastTimeStamp = {}
                timeStamp = datetime.strftime(row[0], "%Y-%m-%d %H:%M:%S")
                message = row[1]
                myFullValue = MyCassandraData(timeStamp,message)
                cass_session.execute(f"INSERT INTO {cassandra_table} (timeStamp, message) VALUES (%s, %s)",
                                    (myFullValue.timeStamp, myFullValue.message))
                lastTimeStamp = {myFullValue.timeStamp:myFullValue.message}
            with open(myJsonFile, 'w') as file:
                json.dump(lastTimeStamp, file)
            file.close()
            print(Fore.GREEN + successMessage)
            sleep(sleepTime)
        except:
            print(Fore.RED + errorMessageCass)
            sleep(reload)

if __name__ == '__main__':
    sendDataToCassandra()
        
    
        
