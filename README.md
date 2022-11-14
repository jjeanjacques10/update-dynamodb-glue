# Update DynamoDB with AWS Glue

This is a sample project to demonstrate how to update DynamoDB with AWS Glue. On this table there are no one pokemon category, so we need to filter the data and update each row with the correct category from the [pokemon API](https://pokeapi.co/).

| number | name |
| ------ | ---- |
| 1 | Bulbasaur |
| 2 | Ivysaur |
| 3 | Venusaur |
| 4 | Charmander |
| 5 | Charmeleon |
| 6 | Charizard |

## How to run

### 1. Create a DynamoDB table

Create a DynamoDB table with the following schema.

| field | description |
| ----- | ----------- |
| number | The pokemon number |
| name | The pokemon name |

### 2. Create a Glue job

Create a Glue job with the following settings.

- Job type: Spark
- Job language: Python
- Glue version: 2.0
- Number of workers: 2

### 3. Run the Glue job on AWS Console

### 4. Check the DynamoDB table

You can see the following records in the DynamoDB table.

| number | name | category |
| ------ | ---- | -------- |
| 1 | Bulbasaur | grass |
| 2 | Ivysaur | grass |
| 3 | Venusaur | grass |
| 4 | Charmander | fire |
| 5 | Charmeleon | fire |
| 6 | Charizard | fire |

## References

- [AWS Glue](https://aws.amazon.com/glue/)
- [PySpark Glue Tutorial](https://github.com/johnny-chivers/pyspark-glue-tutorial)
- [How to export an Amazon DynamoDB table to Amazon S3 using AWS Step Functions and AWS Glue](https://aws.amazon.com/blogs/big-data/how-to-export-an-amazon-dynamodb-table-to-amazon-s3-using-aws-step-functions-and-aws-glue/)

---
Developed by [Jean Jacques Barros](https://github.com/jjeanjacques10)
