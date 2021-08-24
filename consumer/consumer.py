from pyspark import SparkConf
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, round

def main():
    conf = SparkConf() # initialise the spark session as an entry point to spark sql functionality
    conf.setMaster('local[*]')
    spark = SparkSession.builder.config(conf=conf).config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    # create a schema to parse the json data from the value field of the kafka topic message.
    schema = StructType([ \
    StructField("ts",StringType(),True), \
    StructField("symbol",StringType(),True), \
    StructField("price",FloatType(), True) \
    ])

    # read the messages from the kafka topic by correctly configuring the input options
    df = spark.read.format('kafka').option("kafka.bootstrap.servers", "kafka:9092").option('subscribe', 'prices').option("startingOffsets", "earliest").load()
    json_df=df.select(from_json(F.col("value").cast("string"), schema).alias("data")).select("data.*")
    json_df.printSchema()
    json_df.show(truncate=False)

    message_count = json_df.count() # find the total number of messages using count and print the output
    print(f'Number of messages in this topic: {message_count}\n')

    # find the average, min, max and stddev of the price column grouped by symbol
    compute_df = json_df.groupBy('symbol').agg(F.avg("price").alias("avg_price"), F.max("price").alias("max_price"), F.min("price").alias("min_price"), F.stddev("price").alias("stddev_price"))
    compute_df.select("symbol", round("avg_price",2).alias("avg_price") , round("max_price",2).alias("max_price"), round("min_price",2).alias("min_price"), round("stddev_price",2).alias("stddev_price")).show()


    data_collection = compute_df.collect() # collect the computed values in to a dictionary to use as a filter to print outliers
    filter_dictionary = {}
    for row in data_collection:
        filter_dictionary[row['symbol']] = (row['avg_price'], row['stddev_price'])
    
    outlier_list = [] # create an outlier list to collect all rows that are outliers based on the z = (price - mean)/std equation /
    for row in json_df.collect(): # outliers were chosen in order to not satisfy -3<=z<=3
        z_val = (row['price'] - filter_dictionary[row['symbol']][0])/filter_dictionary[row['symbol']][1]
        if abs(z_val) > 3:
            outlier_list.append(row)
    outlier_df = spark.createDataFrame(outlier_list) # create a dataframe out of the outlier rows and print it
    outlier_df.select("ts", "symbol", round("price",2).alias("price")).show(truncate=False)

if __name__ == "__main__":
    main()