import sys
import os
import requests
from awsglue.dynamicframe import DynamicFrame
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

TABLE_NAME = "tb_pokemons"

dyf = glueContext.create_dynamic_frame.from_options(
    connection_type="dynamodb",
    connection_options={
        "dynamodb.input.tableName": TABLE_NAME,
        "dynamodb.throughput.read.percent": "1.0",
        "dynamodb.splits": "100"
    }
)

print(f"Count Items: {dyf.count()}")
print(f"Items:")
dyf.show()

filtered_dyf = dyf.filter(f=lambda x: "category" not in x)

print(f"Count Items without category: {filtered_dyf.count()}")
print(f"Items without category:")
filtered_dyf.show()


def add_category(row):
    url = f"https://pokeapi.co/api/v2/pokemon/{row['number']}"

    row["category"] = requests.get(url).json()["types"][0]["type"]["name"]
    return row


# Filter out the rows that no have category
updated_dyf = filtered_dyf.map(add_category)
updated_dyf.printSchema()

# Show date filtered
updated_dyf.show()

if filtered_dyf.count() < 1:
    print('There are no items to process')
    os._exit(0)
else:
    print('There are items to process')
    # Update the table
    new_data = DynamicFrame.fromDF(updated_dyf.toDF(), glueContext, "new_data")

    write_df = glueContext.write_dynamic_frame_from_options(
        frame=new_data,
        connection_type="dynamodb",
        connection_options={
            "dynamodb.output.tableName": TABLE_NAME,
            "dynamodb.throughput.write.percent": "1.0"
        },
        transformation_ctx="write_df"
    )

    job.commit()
