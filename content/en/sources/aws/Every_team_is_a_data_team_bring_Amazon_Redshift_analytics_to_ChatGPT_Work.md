---
title: Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work
description: The AWS Data Analytics plugin for ChatGPT Work brings Amazon Redshift analytics to business teams, enabling natural-language questions against governed data warehouses and data lakes, with dashboard creation and shareable results.
date: 2026-09-10
tags: [aws, data-analytics, chatgpt, redshift, business-intelligence, natural-language-sql]
locale: en
source_url: "https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/"
blog: aws
---

# Every team is a data team — bring Amazon Redshift analytics to ChatGPT Work

**Authors**: AWS Big Data Blog · **Published**: Sep 10, 2026 · **Source**: [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/every-team-is-a-data-team-bring-amazon-redshift-analytics-to-chatgpt-work/)

## About the AWS Data Analytics plugin

Today, AWS is announcing the [AWS Data Analytics plugin](https://chatgpt.com/plugins/plugin_asdk_app_6a917708c64481918f7ddea0cef4b8e6?q=aws) for the new [Data agent](https://chatgpt.com/plugins/Plugin_fc9843a6fb34819195d6c7802398a8a7) in ChatGPT Work. The plugin helps teams across an organization ask questions in natural language, analyze governed data across their Amazon Redshift data warehouse and data lakes, and create shareable dashboards. All this happens from a conversation in ChatGPT Work.

Tens of thousands of customers choose Amazon Redshift every day to run their most demanding workloads, because it delivers analytics at scale with industry-leading price performance. Customers love how Amazon Redshift provides access to their data warehouses and data lakes together in one place. Teams can combine curated business data with the broader operational, historical, and third-party data stored in open formats like Apache Iceberg in their data lakes. This gives them a complete picture to make business-critical decisions across their data.

## Why the plugin was built

Customers have asked AWS for a way to put that trusted data in the hands of more of their people. That means not only the analysts and engineers who write SQL, but also the sales leaders, operations managers, and finance teams who depend on the results. A sales leader wants to know how the customer pipeline has changed this quarter. An operations manager wants to understand why fulfillment times changed over the past month. That's why we built the AWS Data Analytics plugin, bringing the power of Amazon Redshift and AWS analytics to ChatGPT Work.

> **"Business teams can make decisions faster when they can source their own analytics and build the dashboards they need. Our work with AWS gives more people that ability, helping them understand changes in performance and decide where to focus. The AWS Data Analytics plugin connects Amazon Redshift to the Data agent in ChatGPT Work, so employees can analyze trusted company data simply by asking, with their organization's existing access controls in place."**

— Arpan Shah, General Manager, Technology at OpenAI

## How it works

The new plugin helps shorten the path from question to decision for everyone. Using the Data agent in ChatGPT Work, employees can explore the data they are authorized to access in Amazon Redshift by asking questions in everyday language. They can then refine the analysis, investigate changes, and turn the results into a dashboard without leaving ChatGPT Work. The plugin works with both Amazon Redshift provisioned clusters and Serverless workgroups. Customers can integrate it into their existing multi-cluster or multi-workgroup environments and benefit from the cost and security controls they've already set up.

### Conversational workflow

Consider Maya, a business analyst supporting a revenue operations team. She wants to understand the revenue performance across various segments and regions.

Maya starts by loading the AWS Data Analytics plugin in ChatGPT Work, and then asking:

> *"What are the revenue metrics for the past 30 days compared to the previous 30-day period?"*

[![ChatGPT Work conversation asking for revenue metrics in ChatGPT Work using the AWS Data Analytics plugin](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-1.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-1.png)

*Figure 1: Asking for revenue metrics in ChatGPT Work using the AWS Data Analytics plugin*

The plugin translates her question into SQL, or a sequence of queries if needed, and runs them against the relevant data in Amazon Redshift. It returns key revenue performance metrics based on the same curated revenue data that her analytics team maintains.

[![Table of revenue performance metrics the plugin returned from Amazon Redshift](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-2.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-2.png)

*Figure 2: Revenue performance metrics returned from Amazon Redshift*

Maya notices that gross margin is declining and asks a follow-up question:

> *"What is my revenue breakdown by product category and region for the past 90 days?"*

[![Revenue results segmented by product category and region for the past 90 days in ChatGPT Work](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-3.png)](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/09/09/BDB-6266-3.png)

*Figure 3: Revenue breakdown by product category and region for the past 90 days*

The plugin carries the context forward, segments the results, and helps Maya understand each segment's performance for the past 90 days. She can inspect the analysis and ask additional questions to drill down even further to understand why certain regions are lagging or why certain segments are outperforming others.

This conversational workflow doesn't replace the data models, metric definitions, or governance practices that the analytics team has established. It helps more employees use that data directly, giving analysts more time for high-value work.

## Plugin capabilities

During a conversation, the AWS Data Analytics plugin can:

* **Discover schemas, tables, columns, and data types** available to the user.
* **Translate a natural-language question** into Amazon Redshift SQL.
* **Run the query** against the customer's Amazon Redshift environment.
* **Present the results** in a table or concise explanation.
* **Use follow-up questions** to filter, compare, or drill into the results.
* **Turn an analysis into an interactive dashboard** that teams can share and explore.

Because the analysis runs against the customer's existing data, teams can continue to use the curated datasets and business definitions they already maintain in Amazon Redshift. Customers whose Amazon Redshift environments query data in both a warehouse and a data lake can also make that data available through the governed datasets exposed to the plugin. The AWS Data Analytics plugin also supports our broader AWS data and analytics services. This includes the ability to work with AWS Glue Data Catalog, Amazon S3 Tables, Amazon Athena, and vector search on AWS.

## Getting started

To get started, install the AWS Data Analytics plugin in ChatGPT Work to connect it to Amazon Redshift. Give your teams a conversational path to governed insights across your data warehouse and data lake today.

To learn more, see the following resources:

* [AWS Data Analytics plugin](https://chatgpt.com/plugins/plugin_asdk_app_6a917708c64481918f7ddea0cef4b8e6?q=aws)
* [Data agent in ChatGPT Work](https://chatgpt.com/plugins/Plugin_fc9843a6fb34819195d6c7802398a8a7)
* [OpenAI's announcement](https://openai.com/index/put-data-to-work/)

## About the authors

### Resources

* [Amazon Athena](/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon EMR](/blogs/big-data/category/analytics/amazon-emr?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Kinesis](/blogs/big-data/category/analytics/amazon-kinesis?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon MSK](/blogs/big-data/category/analytics/amazon-managed-streaming-for-apache-kafka/)
* [Amazon QuickSight](/blogs/big-data/category/analytics/amazon-quicksight?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [Amazon Redshift](/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
* [AWS Glue](/blogs/big-data/category/analytics/aws-glue?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

### Follow

* [Twitter](https://twitter.com/awscloud)
* [Facebook](https://www.facebook.com/amazonwebservices)
* [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
* [Twitch](https://www.twitch.tv/aws)
* [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)