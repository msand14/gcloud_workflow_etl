from pyspark.sql.types import *
import pyspark.sql.functions as sfunc
from pyspark.sql.session import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()

raw_files_path = 'gs://youtube-videos-processing/raw/categories'
bronze_output_path = 'gs://youtube-videos-processing/bronze/categories'

df = spark.read.option("multiline", "true") \
      .json(raw_files_path)

df = df.withColumn('nested_items', (sfunc.explode(df.items)))
df = df.select('nested_items.*')
df = df.select('etag', 'id', 'kind', 'snippet.*')

df.write.mode("overwrite").save(bronze_output_path)
