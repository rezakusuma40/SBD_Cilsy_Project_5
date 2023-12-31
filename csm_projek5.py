from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import from_json, col, udf
import re

spark=SparkSession.builder\
    .appName("projek5")\
    .master("local[*]")\
    .getOrCreate()
#   .config("spark.jars.packages",
#   "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,
#   org.elasticsearch:elasticsearch-spark-30_2.12:8.5.2")\
spark.sparkContext.setLogLevel("ERROR")

df=spark.readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .option("subscribe", "projek5")\
    .option("startingOffsets","latest")\
    .option("failOnDataLoss", "false")\
    .load()

mySchema=StructType([
            StructField("id", StringType(), True),
            StructField("user_name", StringType(), True),
            StructField("created_at", StringType(), True),
            StructField("text", StringType(), True),
            StructField("language", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("user_location", StringType(), True),
            ])
df2=df.select(from_json(df.value.cast("string"), mySchema).alias("tweet")).select("tweet.*")

def  cleanTweet(tweext):
    # remove links
    tweext=re.sub(r'http\S+', '', tweext)
    tweext=re.sub(r'bit.ly/\S+', '', tweext)
    tweext=tweext.strip('[link]')
    # remove users
    tweext=re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweext)
    tweext=re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweext)
    # remove punctuations
    my_punctuation='!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@â'
    tweext=re.sub(r'\n+', '', tweext)
    # tweext=re.sub('\u[A-Za-z0-9-_]+', '', tweext)
    tweext=re.sub('['  +  my_punctuation  +  ']+', ' ', tweext)
    # remove hashtag
    tweext=re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', tweext)
    return tweext
 
convertUDF=udf(lambda  z: cleanTweet(z))
df_final=df2.select(col("id"),col("user_name"),col("created_at"),
convertUDF(col("text")).alias("text"),col("language"),
col("user_id"),col("user_location"),)
 
hdfs_path='covid_tweets/'
checkpointhdfs='checkpoint_hdfs/'
query1=df_final.writeStream\
        .outputMode('append')\
        .queryName('writing_to_hdfs')\
        .format('csv')\
        .option('path', hdfs_path)\
        .option('checkpointLocation', checkpointhdfs)\
        .start()

checkpointelk='checkpoint_elk/'
indexelk='covid_tweets_project5'
query2=df_final.writeStream\
        .outputMode('append')\
        .queryName('writing_to_es')\
        .format('org.elasticsearch.spark.sql')\
        .option('checkpointLocation', checkpointelk)\
        .option('es.resource', indexelk)\
        .option('es.nodes','localhost')\
        .option('es.port','9200')\
        .start()

spark.streams.awaitAnyTermination()