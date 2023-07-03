# kafka_postgres_cassandra

This project consists of three Python files, an INI file, two text files, and a JSON file. It involves data processing and transfer between Kafka, PostgreSQL, and Cassandra.

## File Descriptions

1. **myProducer.py**: This file contains a Kafka producer that generates data and sends it to a Kafka topic based on the configuration provided in the `myConfig.ini` file.

2. **kafkaToPostgres.py**: This file contains a Kafka consumer that consumes data from a Kafka topic and stores it in a PostgreSQL database. The configuration details are specified in the `myConfig.ini` file.

3. **postgresToCassandra.py**: This file retrieves data from a PostgreSQL database and sends it to a Cassandra database. It utilizes the configuration details from the `myConfig.ini` file.

4. **myConfig.ini**: This INI file contains the configuration parameters for Kafka, PostgreSQL, and Cassandra, such as server details, topic names, table names, and error messages.

5. **requirements.txt**: This file lists the required Python packages and their versions necessary to run the project.

6. **cliCommends.txt**: This file provides helpful commands for managing Kafka, PostgreSQL, and Cassandra servers, including starting and stopping servers, creating topics/tables, inserting data, and more.

7. **saveCassandra.json**: This JSON file is used by the `postgresToCassandra.py` script to keep track of the last processed timestamp.

## Instructions

1. Install the required Python packages listed in `requirements.txt`. You can use the following command:
pip install -r requirements.txt

2. Set up and start the necessary server components. Refer to `cliCommends.txt` for instructions on starting Kafka, PostgreSQL, and Cassandra servers.

3. Configure the `myConfig.ini` file according to your server and topic/table details.

4. Run the scripts in the following order:

a. Start the Kafka producer:
   ```
   python myProducer.py
   ```

b. Start the Kafka consumer and PostgreSQL data transfer:
   ```
   python kafkaToPostgres.py
   ```

c. Start the PostgreSQL to Cassandra data transfer:
   ```
   python postgresToCassandra.py
   ```

5. Monitor the console for success or error messages from each script.

Note: Make sure you have the necessary permissions and access rights for the server components and databases.

Please refer to the individual script files for more detailed information about their functionality and implementation.

Feel free to customize the scripts and configurations as per your specific requirements.

If you encounter any issues or have further questions, please don't hesitate to reach out for support.

Happy coding!
