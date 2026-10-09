---
title: "Build declarative ETL pipelines with AWS Glue 6.0"
source_url: "https://aws.amazon.com/blogs/big-data/build-declarative-etl-pipelines-with-aws-glue-6-0/"
blog: "AWS Big Data"
published: "2026-09-09"
locale: "en"
---

# Build declarative ETL pipelines with AWS Glue 6.0

by Syed Humair , Bo Li , Kartik Panjabi , and Shrey Malpani on 09 SEP 2026 in Advanced (300) , AWS Glue , Technical How-to Permalink Share
Data teams commonly build the extract, transform, and load (ETL) pipelines that turn raw order events into analyst-ready aggregates as a bronze, silver, and gold sequence, the medallion architecture.
Bronze holds raw ingested records, silver holds cleaned and validated data, and gold holds the business-level aggregates that analysts query.
Today you build this on AWS Glue with an orchestrator such as Amazon Managed Workflows for Apache Airflow (Amazon MWAA) or AWS Step Functions coordinating the stages. Many teams run production pipelines exactly this way.
As a pipeline grows, the coordination work grows with it: you wire job dependencies, manage intermediate checkpoints, and add retry logic stage by stage.
AWS Glue 6.0 , powered by [Apache Spark 4.1](https://spark.apache.org/docs/4.1.1/) , introduces [Spark Declarative Pipelines](https://docs.aws.amazon.com/glue/latest/dg/spark-declarative-pipelines.html) (SDP), which simplifies this further.
Instead of orchestrating jobs by hand, you declare what each dataset should contain and let the declarative framework resolve dependencies, manage checkpoints, and orchestrate execution order automatically.
The result runs as a single declarative job, with no manual directed acyclic graph (DAG) wiring or imperative orchestration code.
In this post, you build a single AWS Glue 6.0 job that turns raw order records into validated, aggregated, analytics-ready tables through the bronze, silver, and gold sequence. You do this without writing any orchestration logic.
This walkthrough uses the AWS Command Line Interface ( AWS CLI ), and the same operations are available through the AWS SDKs .

## Solution overview
You build a single AWS Glue 6.0 job that reads raw order records from a CSV file in Amazon Simple Storage Service ( Amazon S3 ). The job flows them through three declared datasets.
These are a bronze materialized view (ingest as-is), a silver materialized view (type, validate, and classify), and a gold SQL materialized view (aggregate by region).
With [AWS Glue Data Catalog](https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html) integration turned on, all three land as Data Catalog tables, queryable with standard SQL tooling such as Amazon Athena .
SDP resolves the dependency order from the dataset references in your code, so you never orchestrate the steps yourself.

## Two ways to build the pipeline
Before you build the pipeline, let’s understand this new way of writing ETL pipelines with a quick comparison of the imperative and declarative approaches.

...

Compared to that, the declarative approach runs as a single ETL job with SDP. The following diagram mirrors the previous one, but here it is a single AWS Glue ETL job instead of three jobs plus an orchestrator.
[Declarative pipeline: a single AWS Glue job running the bronze, silver, and gold layers with Spark Declarative Pipelines.](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/03/BDB-6104-2.png)
Figure 2: The declarative pipeline, a single AWS Glue job running the bronze, silver, and gold layers with SDP.
The declarative approach reduces more than the number of jobs. It removes the boilerplate that surrounds them. An orchestrator such as Amazon MWAA or AWS Step Functions already handles retries and parallelism, but only at the granularity of a whole job.

...

SDP separates the _what_ from the _how_ : you declare **datasets** (the outputs you want), and SDP builds the **flows** that produce them and runs them as one **pipeline** , resolving dependencies and execution order automatically.
You declare these abstractions through Python decorators. This post covers three of them, `@dp.table` , `@dp.materialized_view` , and `@dp.temporary_view` , each with its own purpose:

...

Streaming tables append only new arrivals. Materialized views fully recompute. This post uses `@dp.materialized_view` for all three layers to keep the walkthrough focused.
In production, you would typically use `@dp.table` for the bronze layer to process only new files as they arrive rather than re-reading the full source each run.

...

### Running and refreshing the pipeline
* `--refresh <datasets>` updates only the named datasets (comma-separated, no spaces).
* `--full-refresh <datasets>` resets and recomputes only the named datasets (for streaming tables, this also clears their checkpoints).
* `--full-refresh-all` resets and recomputes every dataset in the pipeline.

...

```\n# Full reset and recompute of the entire pipeline\naws glue start-job-run \\\n  --job-name \"${JOB_NAME}\" \\\n  --arguments '{\"--conf\":\"spark.glue.sdp.jobMode=RUN --conf spark.glue.sdp.runMode=--full-refresh-all\"}' \\\n  --region \"${AWS_REGION}\"\n```
Selective refresh is useful during development, so you can iterate on a single layer without reprocessing the entire graph. Note that `--refresh` and `--full-refresh` each take an explicit list of datasets. To reset the whole pipeline, use `--full-refresh-all` .

...

### Materialized views: Batch transforms with automatic dependency resolution
Materialized views recompute their full result set on each run. SDP infers dependencies from table references: in this pipeline, `silver_orders` references `bronze_orders` , so SDP runs bronze first, as shown in the following diagram.

...

The silver layer references `bronze_orders` through `spark.table(\"bronze_orders\")` , with no explicit dependency declaration. SDP builds the DAG by analyzing table references in your code and runs bronze first automatically.
Bronze reads every column as a string by design: the bronze layer preserves raw source data without coercion. Type casting, validation, and filtering happen in the silver layer.

...

### SQL and Python coexistence
```\nCREATE MATERIALIZED VIEW gold_sales_summary\nCOMMENT 'Completed-order metrics by region'\nAS\nSELECT\n  region,\n  COUNT(*) AS order_count,\n  CAST(ROUND(SUM(amount), 2) AS DECIMAL(10, 2)) AS total_sales,\n  CAST(ROUND(AVG(amount), 2) AS DECIMAL(10, 2)) AS average_order_value\nFROM silver_orders\nGROUP BY region;\n```
In this post, Python files define ingestion and validation logic, and SQL files define reporting views and aggregations. SDP discovers both through the `libraries` glob pattern in the pipeline specification and resolves the cross-language dependencies automatically.
The complete source for all three layers follows in the step-by-step walkthrough.

## Build the pipeline: Step by step
The rest of this post is a hands-on walkthrough. You build a single AWS Glue 6.0 job that reads `orders.csv` and processes it through the bronze, silver, and gold layers. The steps are:
1. **Prerequisites** : AWS account, AWS Identity and Access Management (IAM) role, and S3 bucket.
2. **Set up sample data** : create `orders.csv` and upload it to Amazon S3.
3. **Build the pipeline files** (the `spark-pipeline.yml` specification plus the three transformation files).
4.
**Package the pipeline** into a zip and upload it to Amazon S3.
5. **Create the database** : a Data Catalog database with an S3 location.
6. **Configure the job** : create the AWS Glue 6.0 job with the SDP flag.
7. **Validate** : run in dry-run mode to verify the graph.
8.
**Run the pipeline** to materialize all datasets.
9. **Query results** : inspect the tables with Amazon Athena.
10. **Clean up** : delete the resources you created.

...

## Step 1 – Prerequisites
### IAM role for the pipeline
Attach the AWS managed policy **AWSGlueServiceRole** , which grants the AWS Glue Data Catalog and Amazon Cloudwatch Logs access the job needs.
Then add an inline policy that scopes Amazon S3 access to your bucket, covering the input data, the pipeline zip, the pipeline storage (state) path, and the warehouse location:

...

For a full breakdown of the baseline permissions, see [Setting up IAM permissions for AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/set-up-iam.html) .

...

## Step 2 – Set up sample data
The AMER and EMEA regions each have two completed orders, so the gold layer’s `order_count` and `average_order_value` are meaningful aggregations rather than single-row passthroughs.

...

## Step 3 – Build the pipeline files
The complete contents of each file follow.

### 3a. spark-pipeline.yml
The specification names the pipeline, points to the Data Catalog database, configures state storage, and discovers transformation files. As with the transformation files, it uses the `__DATABASE__` , `__BUCKET__` , and `__PREFIX__` tokens, which you substitute at packaging time in Step 4:

```\nname: simple_sdp_demo\ncatalog: spark_catalog\ndatabase: __DATABASE__\nstorage: s3://__BUCKET__/__PREFIX__/state/\\nlibraries:\n  - glob:\n      include: transformations/**\nconfiguration:\n  spark.sql.shuffle.partitions: \"4\"\n```

### 3b. transformations/01_bronze.py
Bronze preserves the raw source as strings. No coercion, no filtering:

...

You substitute the tokens with your real values when you package the project in Step 4, which keeps every file consistent with the variables you exported in Step 1.

### 3c. transformations/02_silver.py
Silver casts types, filters to complete orders with positive amounts, and derives an `amount_band` classification:
```\n\"\"\"Silver layer: type, validate, and classify complete orders.\"\"\"\nfrom pyspark import pipelines as dp\nfrom pyspark.sql import DataFrame, SparkSession\nfrom pyspark.sql.functions import col, to_timestamp, trim, when\n\nspark = SparkSession.active()\n\n@dp.materialized_view(comment=\"Validated complete orders with typed values\")\ndef silver_orders() -> DataFrame:\n    typed = (\n        spark.table(\"bronze_orders\")\n        .select(\n            trim(col(\"order_id\")).alias(\"order_id\"),\n            trim(col(\"customer_id\")).alias(\"customer_id\"),\n```\n\n...\n\n```\n            col(\"order_id\").isNotNull()\n            & col(\"region\").isNotNull()\n            & col(\"order_ts\").isNotNull()\n            & (col(\"status\") == \"COMPLETE\")\n            & (col(\"amount\") > 0)\n        )\n    )\n    return typed.select(\n        \"*\",\n        when(col(\"amount\") >= 500, \"large\")\n```\n\n...\n\n## Step 4 – Package the project
```\n    spark-pipeline.yml > build/package/spark-pipeline.yml\n\nsed -e \"s|__BUCKET__|${BUCKET}|g\" \\\n    -e \"s|__PREFIX__|${PREFIX}|g\" \\\n    transformations/01_bronze.py > build/package/transformations/01_bronze.py\ncp transformations/02_silver.py transformations/03_gold.sql build/package/transformations/\n\n```\n\n...\n\n## Step 5 – Create the database
The database named in `spark-pipeline.yml` must already exist in the AWS Glue Data Catalog, with an S3 location URI, before the pipeline runs. SDP does not create it automatically:

...

## Step 6 – Configure the job
Create an AWS Glue 6.0 job with the zip as `ScriptLocation` and the SDP flag enabled:

...\n\n```\n--default-arguments \"{\\\"--enable-spark-declarative-pipeline\\\":\\\"true\\\",\\\"--enable-glue-datacatalog\\\":\\\"true\\\"}\" \\\n--region \"${AWS_REGION}\"\n```
...

| **Argument** | **Purpose** |
| `--enable-spark-declarative-pipeline` | Activates the SDP executor (required) |
| `ScriptLocation` | Points to the pipeline zip, not a .py file |
_Table 2: Key arguments for the create-job command._

...

No other change is needed, and the `--enable-spark-declarative-pipeline` flag stays the same. The zip keeps the upload to a single object.

## Step 7 – Validate (dry run)
Run the job in validation mode first to verify the dependency graph without materializing data:
```\naws glue start-job-run \\\n  --job-name \"${JOB_NAME}\" \\\n  --arguments '{\"--conf\":\"spark.glue.sdp.jobMode=VALIDATE\"}' \\\n  --region \"${AWS_REGION}\"\n```
Validation analyzes the project structure, dependency graph, and SQL and Python compilation without creating tables, executing transforms, or writing data. Confirm that the database has no tables after validation completes.

...

## Step 8 – Run the pipeline
Start the pipeline in normal execution mode:
```\naws glue start-job-run \\\n  --job-name \"${JOB_NAME}\" \\\n  --arguments '{\"--conf\":\"spark.glue.sdp.jobMode=RUN\"}' \\\n  --region \"${AWS_REGION}\"\n```
After the run completes, list the materialized tables:

...

## Cost considerations
This walkthrough runs on 2 G.1X workers (2 DPUs), reads a 6-row CSV, and completes each run in about 2 minutes. It produces three tables in one AWS Glue Data Catalog database.

...

## What’s next
* **Extend** : Add transformation stages (additional `@dp.materialized_view` functions) and connect them by referencing upstream tables. The pipeline picks up the new dependency automatically.

...

## Conclusion
In this post, you used Spark Declarative Pipelines, the declarative alternative to explicitly orchestrated ETL, now available in AWS Glue 6.0. Two decorated Python functions and one SQL file define the bronze, silver, and gold datasets, and SDP resolves the dependencies and manages execution order for you.
With SDP, you declare what each dataset should contain and the declarative framework handles ordering and execution. A three-layer pipeline that would otherwise need separate transform and orchestration logic runs as one job that you can ship and maintain.
To get started, open the [AWS Glue console](https://console.aws.amazon.com/glue/home) and build the walkthrough pipeline, or adapt the pattern to your own bronze, silver, and gold datasets. For the full set of features, see the AWS Glue 6.0 launch announcement .

...

## About the authors
### Bo Li
Bo is a Senior Software Development Engineer on the AWS Glue team. He is devoted to designing and building end-to-end solutions to address customers’ data analytic and processing needs with cloud-based, data-intensive and generative AI technologies.
Kartik Panjabi

### Kartik Panjabi
Kartik is a Software Development Manager on the AWS Glue team. His team builds generative AI features for data integration and distributed systems for data integration.
[Create an AWS account](https://signin.aws.amazon.com/signup?request_type=register)