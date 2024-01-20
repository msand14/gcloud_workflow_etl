from pyspark.sql.types import *
import pyspark.sql.functions as sfunc
from pyspark.conf import SparkConf
from pyspark.sql.session import SparkSession
import pyspark
from pyspark import SparkContext

spark = SparkSession.builder.master("local[*]").getOrCreate()

bronze_input_path = 'gs://youtube-videos-processing/bronze/categories'
silver_output_path = 'gs://youtube-videos-processing/silver/categories'

df = spark.read.parquet(bronze_input_path)

df = df.dropDuplicates()

df = df.withColumnRenamed('channelID', 'channel_id')

df.write.mode("overwrite").save(silver_output_path)
