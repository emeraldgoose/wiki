---
title: "How to migrate from Amazon CloudSearch to Amazon OpenSearch Serverless"
source_url: "https://aws.amazon.com/blogs/big-data/how-to-migrate-from-amazon-cloudsearch-to-amazon-opensearch-serverless/"
blog: "AWS Big Data"
published: "2026-09-10"
locale: "en"
tags: [source, aws-big-data, infrastructure]
---

# How to migrate from Amazon CloudSearch to Amazon OpenSearch Serverless

If you run search on [Amazon CloudSearch](https://aws.amazon.com/cloudsearch/), now is the time to plan your migration to [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/serverless/). Modern search has moved on to capabilities beyond what CloudSearch provides: semantic and hybrid search, Retrieval Augmented Generation (RAG), and agentic search. OpenSearch Serverless gives you all of these with automatic scaling on a pay-for-what-you-use basis. You don’t need to choose or maintain infrastructure. OpenSearch Serverless maintains the hands-off, operational simplicity of CloudSearch.

This post shows you how to migrate your CloudSearch domain to an [Amazon OpenSearch Serverless](https://aws.amazon.com/opensearch-service/) collection. We walk you through assessing your CloudSearch configuration, creating an OpenSearch Serverless collection with explicit index mappings, converting your documents and queries, configuring security policies, loading your data with Amazon OpenSearch Ingestion, and validating the migration before cutting over.

### Key differences to note

- **Independent scaling** – OpenSearch Serverless scales indexing and search compute independently and can scale compute to zero when a collection is idle (you still pay for storage). For the cost structure, see [Managing capacity limits for Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-scaling.html).

- **Layered security model** – OpenSearch Serverless applies encryption, network, and data access policies at separate layers. For the security model, see [Security in Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-security.html).

## Prerequisites

To follow along with this post, you need the following:

- An AWS account.
- An existing Amazon CloudSearch domain with indexed data.
- Source data available in a durable store such as [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/) or [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) (CloudSearch doesn’t provide a built-in export or backup feature, so your original source data is required to re-ingest into OpenSearch).
- AWS Identity and Access Management (IAM) permissions to create and manage Amazon OpenSearch Serverless collections, encryption policies, network policies, and data access policies.
- An Amazon OpenSearch Ingestion pipeline (or alternative ingestion method) for loading data.

## Plan the migration

Planning is where you decide what success means: minimal downtime, no data loss, current functionality preserved, and custom configurations carried over. You don’t need to plan for infrastructure because OpenSearch Serverless provisions and scales compute for you. Your main planning task is to assess your current CloudSearch configuration so you can reproduce its behavior on the target.

Document your existing setup from the Amazon CloudSearch console. Record the current instance type, the partition count, and the replication count. Capture the total document count and overall data size, and record every field definition, including field types and the search, facet, and sort settings for each field. Note any analyzers, synonyms, stopwords, or custom rank expressions. Note whether you use the 2011 or the 2013 CloudSearch API version, because the 2013 API added faceting and filtering features that change how you model the target.

OpenSearch Serverless is the right target for most CloudSearch workloads, but not all of them. If your workload needs very low read-after-write latency (a short refresh interval), tight and predictable query response times, or direct control over instance configuration, choose an [Amazon OpenSearch Service managed clusters deployment instead and size it from your workload profile](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/sizing-domains.html).

The migration involves four main concerns: your source data format, your queries, your field definitions, and your access policies. Before you plan the details, it helps to see the whole migration at once. The following diagram maps the migration across four phases: your source CloudSearch environment, the migration pipeline that converts and moves your data, the OpenSearch Serverless target, and cutover and operations.

![Migration workflow across four phases: source CloudSearch, migration pipeline, OpenSearch Serverless target, and cutover and operations](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-5903-1.png)

Figure 1: The migration workflow across four phases

In the source environment, you assess your CloudSearch configuration and back up your source data (Amazon S3, Amazon DynamoDB, or another store). Note the Source Data Format (SDF), the URL-based query syntax, and the IAM access policies you need to carry over. In the migration pipeline, you map field types, convert the data format from CloudSearch JSON to OpenSearch-compatible JSON, convert your queries to the OpenSearch query domain-specific language (DSL), configure security, bulk-ingest the data, and validate the result. The OpenSearch Serverless target holds the collection, index mappings, ingested documents, and the encryption, network, and data access policies, and it scales with your workload on a pay-for-what-you-use basis. In cutover and operations, you update your application to the new endpoint and clients, monitor with [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/), and decommission CloudSearch once no traffic remains.

## Model your data in OpenSearch Service

OpenSearch Service uses [index mappings](https://opensearch.org/docs/latest/field-types/) to define the fields and data types in an index. Because you know your CloudSearch schema, define the target mapping explicitly when you create the index. Create the index and set its mapping in a single request, and set `dynamic` to `strict` so OpenSearch rejects any document that contains a field you did not define. Strict mapping catches schema drift at ingest time, avoiding the default OpenSearch behavior of creating new mappings for undefined fields.

```json
PUT /imdb_movies
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "title": {
        "type": "text",
        "fields": {
          "keyword": { "type": "keyword" }
        }
      },
      "genres": { "type": "keyword" },
      "rating": { "type": "float" },
      "release_date": { "date" }
      ...
    }
  }
}
```

JSON

### Field type mapping

The following table maps CloudSearch field types to their OpenSearch Service equivalents.

|     |     |     |
| --- | --- | --- |
| **CloudSearch** | **OpenSearch Service equivalent** | **Notes** |
| text | text | Text is tokenized. Stemming, synonyms, and stopwords apply. Good for matching user terms. |
| literal | keyword | Not tokenized. Good for exact-match search. |
| int | integer | Use for ranking, faceting, and narrowing. |
| double | float or double | . |
| date | date | . |
| boolean | boolean | . |
| latlon | geo\_point | . |
| text-array | text | OpenSearch handles arrays natively, so map to the base text type. |

[... middle omitted — see footer ...]


## Clean up

Because you’re migrating to OpenSearch Serverless, the resources that you’ve created will likely become your production resources. If not, delete any OpenSearch Serverless collections and S3 buckets you created to avoid incurring ongoing cost.

## Conclusion

In this post, you saw how Amazon CloudSearch and Amazon OpenSearch Serverless compare, and how the concepts you rely on in CloudSearch (field types, query syntax, autoscaling, and access control) translate into OpenSearch Service. You assess your CloudSearch configuration, model your data with explicit OpenSearch mappings, move your converted documents into the collection with OpenSearch Ingestion, convert your URL-based queries into the OpenSearch query DSL, configure security, and validate before cutover. OpenSearch Serverless gives you the hands-off operational model you have with CloudSearch, and adds richer query capabilities, granular data access policies, and automatic scaling. To get started, create an OpenSearch Serverless collection on the AWS Management Console and follow the steps in this post.

To learn more, see the following resources:

- [Amazon OpenSearch Service Developer Guide](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/)
- [Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)
- [OpenSearch documentation](https://opensearch.org/docs/latest/)
- [Four ways to build with Amazon OpenSearch Service](https://aws.amazon.com/blogs/big-data/four-ways-to-build-with-amazon-opensearch-service/)
- [Amazon OpenSearch Service vector database capabilities explained](https://aws.amazon.com/blogs/big-data/amazon-opensearch-services-vector-database-capabilities-explained/)

* * *

## About the authors

### Resources

- [Amazon Athena](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon EMR](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-emr?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon Kinesis](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-kinesis?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon MSK](https://aws.amazon.com/blogs/big-data/category/analytics/aws-managed-streaming-for-apache-kafka/)
- [Amazon QuickSight](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-quicksight?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon Redshift](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [AWS Glue](https://aws.amazon.com/blogs/big-data/category/analytics/aws-glue?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

* * *

### Follow

- [Twitter](https://twitter.com/awscloud)
- [Facebook](https://www.facebook.com/amazonwebservices)
- [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
- [Twitch](https://www.twitch.tv/aws)
- [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)