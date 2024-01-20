from pyspark.sql.types import *
import pyspark.sql.functions as sfunc
from pyspark.sql.session import SparkSession

spark = SparkSession.builder.master("local[*]").getOrCreate()

bronze_input_path = 'gs://youtube-videos-processing/bronze/videos'
silver_output_path = 'gs://youtube-videos-processing/silver/videos'

df = spark.read.parquet(bronze_input_path)

df = df.dropDuplicates()

format = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"

df = (
    df
    .withColumn('trending_date',
                sfunc.to_date(
                    sfunc.concat(
                        sfunc.lit('20'),
                        sfunc.regexp_replace(
                            sfunc.col('trending_date'),
                            '\.',
                            '-'
                        )
                    ), 'yyyy-dd-MM'
                )
                )
    .withColumn('publish_time',  sfunc.unix_timestamp('publish_time', "yyyy-MM-dd'T'HH:mm:ss.SSS'Z").cast('timestamp'))
    .withColumn('views', sfunc.col('views').astype('int'))
    .withColumn('likes', sfunc.col('likes').astype('int'))
    .withColumn('dislikes', sfunc.col('dislikes').astype('int'))
    .withColumn('comment_count', sfunc.col('comment_count').astype('int'))
    .withColumn('comments_disabled', sfunc.col('comments_disabled').astype('boolean'))
    .withColumn('ratings_disabled', sfunc.col('ratings_disabled').astype('boolean'))
    .withColumn('video_error_or_removed', sfunc.col('video_error_or_removed').astype('boolean'))
)

df = (
    df
    .withColumn(
        'tag',
        sfunc.explode(
            sfunc.split(
                sfunc.col('tags'), '\|'
            )
        )
        )
    .withColumn('tag', sfunc.regexp_replace('tag', '"', ''))
)
df = df.drop('tags')

df = df.withColumn('Country', sfunc.split('filename', '/'))
df = df.withColumn('Country', sfunc.col('Country')[sfunc.size('Country') -1])
df = df.withColumn('Country', sfunc.split('Country', '\.'))
df = df.withColumn('Country', sfunc.col('Country')[0])
df = df.withColumn('Country', sfunc.substring('Country', 1, 2))


df = df.drop('filename')

df = df.dropDuplicates()

df.write.mode("overwrite").save(silver_output_path)
