from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as sfunc

spark=SparkSession.builder \
    .master("local[*]") \
    .getOrCreate()

silver_videos_path = 'gs://youtube-videos-processing/silver/videos'
silver_categories_path = 'gs://youtube-videos-processing/silver/categories'
gold_destiny_path = 'gs://youtube-videos-processing/gold/'

df_videos = spark.read.load(silver_videos_path)
df_categories = spark.read.load(silver_categories_path)



df = (
    df_videos
    .withColumnRenamed('title', 'video_title')
    .alias('vid')
    .join(
        df_categories.alias('cat'),
        df_videos.category_id == df_categories.id,
        'inner'
    )
).select('vid.*', 'cat.title').withColumnRenamed('title', 'category_title')


df = df.drop('tags').dropDuplicates()


df_final = (
    df
    .groupBy(
        'trending_date',
        'Country',
        'category_title'
    )
    .agg(
        sfunc.sum(sfunc.col('views')).alias('views'),
        sfunc.sum(sfunc.col('likes')).alias('likes'),
        sfunc.sum(sfunc.col('dislikes')).alias('dislikes'),
        sfunc.sum(sfunc.col('comment_count')).alias('comments'),
    )
    
)

(
    df_final
    .write
    .mode("overwrite")
    .save(gold_destiny_path)
)