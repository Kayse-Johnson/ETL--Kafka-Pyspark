#%%
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
#%%
conf = pyspark.SparkConf()
conf.setAppName('consumer')
conf.setMaster('local')
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession(sc)
#%%
spark = SparkSession.builder.getOrCreate()
#%%
df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=5, e=6),
    Row(a=2, b=3., c='string2', d=5, e=6),
    Row(a=4, b=5., c='string3', d=7, e=8)
])
#%%
df
#%%
df.show()
df.printSchema()
# %%
df.columns
# %%
for col in df.columns:
    print('nom')
# %%
df.first()
#%%
from pyspark.sql.functions import expr
# %%
df.selectExpr('b AS LOL').show(2)