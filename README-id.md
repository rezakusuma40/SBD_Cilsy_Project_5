Project 5: Muhammad Reza Adi Kusuma
18-12-2022

### Data flow

[![workflow-projek5.png](https://i.postimg.cc/Hxsq4wDy/workflow-projek5.png)](https://postimg.cc/f3pqM0bz)

### Alur pengerjaan:

1. Nyalakan cluster Dataproc
2. Jalankan Elasticsearch dan Kibana
3. Jalankan Zookeeper, lalu jalankan Kafka
4. Jalankan prd_projek5.py
5. Jalankan csm_projek5.py

### Cara menyalakan cluster dataproc:

1. Buka https://console.cloud.google.com/welcome?project=belajar-bigdata
2. Pergi ke Dataproc
3. Checklist cluster yang akan digunakan
4. Klik start, tunggu sampai statusnya menjadi running

### Cara menjalankan Elasticsearch dan Kibana:

1. Pergi ke Compute Engine
2. Klik SSH dari virtual machine yang akan digunakan untuk membuka jendela SSH
3. Di jendela SSH tersebut, untuk menjalankan Elasticsearch ketik command berikut:
   > sudo systemctl daemon-reload
   > sudo systemctl start elasticsearch
4. Di halaman Compute Engine, copy external IP dari virtual machine yang digunakan
5. Buka tab baru di browser
6. Ketik external.IP.VM:9200 di URL (contoh: 35.205.154.5:9200)
7. Di jendela SSH sebelumnya, untuk menjalankan Kibana ketik command berikut:
   > sudo /bin/systemctl daemon-reload
   > sudo /bin/systemctl enable kibana.service
   > sudo /bin/systemctl start kibana.service
8. Buka tab baru di browser
9. Ketik external.IP.VM:5601 di URL (contoh: 35.205.154.5:5601). External IP akan berubah jika virtual machine dinyalakan ulang.

### Cara menjalankan Zookeeper dan Kafka:

1. Di jendela SSH, untuk menjalankan Zookeeper di background ketik command berikut:
   > . apache-zookeeper-3.7.0-bin/bin/zkServer.sh start
2. Jika sudah berhasil, lalu nyalakan Kafka dengan mengetik command berikut:
   > cd kafka_2.12-2.8.2/
   > bin/kafka-server-start.sh config/server.properties

### Menjalankan prd_projek5.py

Persiapan sebelum menjalankan script ini:

1. Perlu memiliki akun twitter developer dulu, jika belum bisa mendaftar di https://developer.twitter.com/.
2. Perlu menjalankan Zookeeper dan Kafka telebih dahulu
3. Perlu membuat topik "projek5" jika belum ada, caranya dengan mengetik command berikut pada jendela SSH
   > cd kafka_2.12-2.8.2/
   > bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic projek5 --partitions 1 --replication-factor 1
4. Menyiapkan file 'twitterAPISulisB.json' berisi key dan token twitter API pribadi di direktori yang sama dengan script ini
   (ini adalah file pribadi saya, tidak saya taruh di repo ini. file ini dapat diganti dengan file serupa)
5. Untuk menjalankan script ini ketik command berikut di jendela SSH:
   > python prd_projek5.py
6. Sebaiknya menggunakan virtual environment, cara mengaktifkan virtual environment dengan mengetik command ini di jendela SSH:
   > . vekafka/bin/activate #vekafka=nama virtual environment saya

### Menjalankan csm_projek5.py

Persiapan sebelum menjalankan script ini:

1. Perlu menginstall Spark dan Hadoop terlebih dahulu (otomatis terinstall saat pembuatan cluster Dataproc)
2. Perlu menjalankan Zookeeper, Kafka, Elasticsearch, dan Kibana terlebih dahulu
3. Sesuaikan jars.packages dengan versi Scala, Spark, dan Elasticsearch
4. Perlu membuat index di Kibana dengan cara:
   - Buka kibana di browser
   - Klik menu -> Management -> Dev Tools
   - di console ketik (jika sudah, lalu tekan ctrl+enter):
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
5. Untuk menjalankan script ini ketik command berikut di jendela SSH:
   > spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.elasticsearch:elasticsearch-spark-30_2.12:8.5.2 csm_projek5.py

### Cek data hasil transformasi

HDFS:

1. ketik command ini pada jendela SSH:
   > hdfs dfs -ls covid_tweets/
2. copy nama salah satu file csv yang terdapat di direktori covid_tweets/ lalu ketik command ini:
   > hdfs dfs -ls covid_tweets/namafile.csv

Elasticsearch:

1. Untuk melihat data yang masuk di Elasticsearch, lebih baik menggunakan Kibana
2. Buka kibana di browser
3. Klik menu -> Management -> Dev Tools
4. Di console ketik (jika sudah, lalu tekan ctrl+enter):
   ```json
   get covid_tweets_project5/_search
   ```
