# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b1e1c8cd-a958-4f59-9822-1dc27ec46183",
# META       "default_lakehouse_name": "LH_Minerals",
# META       "default_lakehouse_workspace_id": "b0973323-41d3-4fc8-8a3b-326e68ad1340",
# META       "known_lakehouses": [
# META         {
# META           "id": "b1e1c8cd-a958-4f59-9822-1dc27ec46183"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import *


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

minerals_schema = StructType([
    StructField("site_name", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("region", StringType(), True),
    StructField("country", StringType(), True),
    StructField("state", StringType(), True),
    StructField("county", StringType(), True),
    StructField("com_type", StringType(), True),
    StructField("commod1", StringType(), True),
    StructField("commod2", StringType(), True),
    StructField("commod3", StringType(), True),
    StructField("oper_type", StringType(), True),
    StructField("dep_type", StringType(), True),
    StructField("prod_size", StringType(), True),
    StructField("dev_stat", StringType(), True),
    StructField("ore", StringType(), True),
    StructField("gangue", StringType(), True),
    StructField("work_type", StringType(), True),
    StructField("names", StringType(), True),
    StructField("ore_ctrl", StringType(), True),
    StructField("hrock_type", StringType(), True),
    StructField("arock_type", StringType(), True)
])

minerals_path = "Files/data/Mineral ores round the world.csv"

df_minerals = spark.read.csv(minerals_path, schema=minerals_schema, sep=",", encoding="UTF-8", header=True)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_minerals= df_minerals.withColumn("commod_array", concat(when((col("commod1").isNotNull()) & (col("commod1")!=""), split(trim(col("commod1")), ",")).otherwise(array()),
when((col("commod2").isNotNull()) & (col("commod2")!=""), split(trim(col("commod2")),",")).otherwise(array()),
when((col("commod3").isNotNull()) & (col("commod3")!=""), split(trim(col("commod3")), ",")).otherwise(array())
))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_minerals= df_minerals.withColumn("commodity", explode(col("commod_array"))) 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

critical_minerals = ["Aluminum","Antimony","Arsenic","Barite","Beryllium","Bismuth","Cerium","Cesium","Chromium","Cobalt","Copper","Dysprosium","Electrical steel","Erbium","Europium","Fluorspar",
    "luorine","Gadolinium","Gallium","Germanium","Graphite","Hafnium","Holmium","Indium","Iridium","Lanthanum","Lithium","Lutetium","Magnesium","Manganese","Natural graphite","Neodymium",
    "Nickel","Niobium","Palladium","Platinum","Praseodymium","REE","Rhodium","Rubidium","Ruthenium","Samarium","Scandium","Silicon","Silicon carbide","Tantalum","Tellurium","Terbium","Thulium",
    "Tin","Titanium","Tungsten","Vanadium","Ytterbium","Yttrium","Zinc","Zirconium"]

df_minerals = df_minerals.filter(col("commodity").isin(critical_minerals))\
                .filter((col("region") == "NA") & (col("country") == "United States")) \
                .withColumnRenamed("oper_type", "operation_type") \
                .withColumnRenamed("dev_stat", "development_status") \
                .select("site_name", "latitude", "longitude", "state", "commodity", "operation_type", "development_status")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

location_window = Window.orderBy(col("site_name"))

df_locations = df_minerals.select("site_name", "latitude", "longitude", "state").distinct() \
                          .withColumn("site_id", row_number().over(location_window))
df_locations = df_locations["site_id", "site_name", "state"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

commodity_window = Window.orderBy(col("commodity"))

df_commodities = df_minerals.select("commodity").distinct() \
                            .withColumn("commodity_id", row_number().over(commodity_window).cast(IntegerType()))
df_commodities = df_commodities["commodity_id", "commodity"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

operations_window = Window.orderBy(col("operation_type"))

df_operations = df_minerals.select("operation_type").distinct() \
                           .withColumn("operation_type_id", row_number().over(operations_window).cast(IntegerType()))
df_operations = df_operations["operation_type_id", "operation_type"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

development_status_window = Window.orderBy(col("development_status"))

df_developments = df_minerals.select("development_status").distinct() \
                    .withColumn("development_status_id", row_number().over(development_status_window).cast(IntegerType()))
df_developments = df_developments["development_status_id", "development_status"]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_minerals= df_minerals.join(df_locations.withColumnRenamed("state", "loc_state"), on="site_name", how="inner")\
                        .join(df_commodities, on="commodity", how="inner") \
                        .join(df_operations, on="operation_type", how="inner") \
                        .join(df_developments, on="development_status", how="inner") \
                        .withColumn("record_date", lit(None).cast(DateType())) \
                        .withColumn("production_volume", lit(None).cast(StringType())) \
                        .select("site_id", "state", "latitude", "longitude", "commodity_id", "operation_type_id", "development_status_id", "production_volume", "record_date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_locations.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("dim_locations")
df_commodities.write.mode("overwrite").saveAsTable("dim_commodities")
df_operations.write.mode("overwrite").saveAsTable("dim_operations")
df_developments.write.mode("overwrite").saveAsTable("dim_developments")
df_minerals.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("fact_minerals")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
