from pyspark.sql.types import *
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from  pyspark.sql.functions import input_file_name

spark=SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()

raw_files_path = 'gs://youtube-videos-processing/raw/videos'
bronze_output_path = 'gs://youtube-videos-processing/bronze/videos'


schema = StructType(
    [
        StructField('video_id', StringType(), True),
        StructField('trending_date', StringType(), True),
        StructField('title', StringType(), True),
        StructField('channel_title', StringType(), True),
        StructField('category_id', StringType(), True),
        StructField('publish_time', StringType(), True),
        StructField('tags', StringType(), True),
        StructField('views', StringType(), True),
        StructField('likes', StringType(), True),
        StructField('dislikes', StringType(), True),
        StructField('comment_count', StringType(), True),
        StructField('thumbnail_link', StringType(), True),
        StructField('comments_disabled', StringType(), True),
        StructField('ratings_disabled', StringType(), True),
        StructField('video_error_or_removed', StringType(), True),
        StructField('description', StringType(), True)
    ]
)

df = (
    spark
    .read
    .format('csv')
    .option("header", True)
    .schema(schema)
    .load(raw_files_path)
)
df = df.withColumn("filename", input_file_name())

df.write.mode("overwrite").save(bronze_output_path)