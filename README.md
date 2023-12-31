Project 5: Muhammad Reza Adi Kusuma
18-12-2022

### Data flow

[![workflow-projek5.png](https://i.postimg.cc/Hxsq4wDy/workflow-projek5.png)](https://postimg.cc/f3pqM0bz)

### Workflow:

1. Turn on Dataproc Cluster
2. Launch Elasticsearch and Kibana
3. Start Zookeeper, then start Kafka
4. Run prd_projek5.py
5. Run csm_projek5.py

### Steps to Run Dataproc Clusters:

1. Visit https://console.cloud.google.com/welcome?project=belajar-bigdata
2. Navigate to Dataproc.
3. Check the cluster you intend to use.
4. Click on "Start" and wait until the status changes to "Running".

### Running Elasticsearch:

1. Access Compute Engine.
2. Open SSH for the respective virtual machine.
3. In the SSH window, execute the following commands:
   > sudo systemctl daemon-reload
   > sudo systemctl start elasticsearch
4. Retrieve External IP from Compute Engine Page.
5. Open a new tab in your browser.
6. Type external.IP.VM:9200 in the URL bar (e.g., 35.205.154.5:9200).

### Running Kibana:

1. In the previous SSH window, execute the following commands:
   > sudo /bin/systemctl daemon-reload
   > sudo /bin/systemctl enable kibana.service
   > sudo /bin/systemctl start kibana.service
2. Open another new tab in your browser.
3. Type external.IP.VM:5601 in the URL bar (e.g., 35.205.154.5:5601).

### Running Zookeeper and Kafka:

1. In the SSH window, to start Zookeeper in the background, type the following command:
   > . apache-zookeeper-3.7.0-bin/bin/zkServer.sh start
2. Once Zookeeper is running successfully, launch Kafka by entering the following commands:
   > cd kafka_2.12-2.8.2/
   > bin/kafka-server-start.sh config/server.properties

### Running prd_projek5.py:

Preparations before executing this script:

1. Ensure a Twitter developer account is available. If not, register at https://developer.twitter.com/.
2. Start Zookeeper and Kafka beforehand.
3. If the "projek5" topic doesn't exist, create it by entering the following commands in the SSH window:
   > cd kafka_2.12-2.8.2/
   > bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic projek5 --partitions 1 --replication-factor 1
4. Prepare the file 'twitterAPISulisB.json' containing the private Twitter API key and token in the same directory as this script.
   (This file is private and won't be included in this repository. Replace it with the relevant file.)
5. To execute this script, type the following command in the SSH window:
   > python prd_projek5.py
6. Using a virtual environment is recommended. Activate the virtual environment by typing the following command in the SSH window:
   > . vekafka/bin/activate #vekafka=nama virtual environment saya

### Running csm_projek5.py:

Preparations before executing this script:

1. Install Spark and Hadoop beforehand (automatically installed during Dataproc cluster creation).
2. Start Zookeeper, Kafka, Elasticsearch, and Kibana before proceeding.
3. Adjust the jars.packages according to the versions of Scala, Spark, and Elasticsearch.
4. Create an index in Kibana by following these steps:
   - Open Kibana in your browser.
   - Navigate to the menu -> Management -> Dev Tools.
   - In the console, type (once ready, press Ctrl+Enter):
   ```json
   PUT covid_tweets_project5
   {
   	"mappings": {
   		"properties": {
   			"id": {
   				"type": "text"
   			},
   			"user_name": {
   				"type": "text"
   			},
   			"created_at": {
   				"type": "date"
   			},
   			"text": {
   				"type": "text"
   			},
   			"language": {
   				"type": "text"
   			},
   			"user_id": {
   				"type": "text"
   			},
   			"user_location": {
   				"type": "text"
   			}
   		}
   	}
   }
   ```
5. To execute this script, type the following command in the SSH window:
   > spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.elasticsearch:elasticsearch-spark-30_2.12:8.5.2 csm_projek5.py

### Checking Transformed Data:

HDFS:

1. Enter the following command in the SSH window:
   > hdfs dfs -ls covid_tweets/
2. Copy the name of any CSV file located in the covid_tweets/ directory, then type this command:
   > hdfs dfs -ls covid_tweets/namafile.csv

Elasticsearch:

1. It's preferable to view data in Elasticsearch using Kibana.
2. Open Kibana in your browser.
3. Navigate to Menu -> Management -> Dev Tools.
4. In the console, type (once ready, press Ctrl+Enter):
   ```json
   get covid_tweets_project5/_search
   ```
