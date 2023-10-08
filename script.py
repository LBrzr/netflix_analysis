from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://172.28.0.2:7077") \
    .appName("Netflix") \
    .getOrCreate()

# Perform Spark operations here

spark.stop()
