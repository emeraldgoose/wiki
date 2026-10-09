---
title: "How Sony LIV built real-time video streaming analytics with AWS"
source_url: "https://aws.amazon.com/blogs/big-data/how-sony-liv-built-real-time-video-streaming-analytics-with-aws/"
blog: "AWS Big Data"
published: "2026-09-08"
locale: "en"
---

# How Sony LIV built real-time video streaming analytics with AWS

_This guest post was co-written with Mukund Acharya from Sony LIV._

Real-time data analytics is transforming how streaming applications understand and serve their audiences. In this post, we share how Sony LIV used Amazon Kinesis Data Streams for sub-second processing and AWS services to build a comprehensive streaming analytics solution on AWS. In this post, we share how SonyLIV built a comprehensive streaming analytics solution on AWS using Amazon Kinesis Data Streams for sub-second event ingestion, Amazon Data Firehose for reliable delivery to storage, Amazon EMR with Apache Spark for scalable batch and micro-batch processing, and Apache Iceberg on Amazon S3 for ACID-compliant, queryable data lake tables. Together, these services enable SonyLIV to capture millions of concurrent viewer events, process them cost-efficiently at scale, and surface actionable insights from real-time engagement metrics to historical trend analysis — all within a fully managed, serverless-friendly architecture.

## About Sony LIV

Sony LIV, operated by Sony Pictures Networks India, is one of India’s leading over-the-top (OTT) streaming applications offering premium content including live sports, original series, movies, and TV shows to millions of users across mobile, web, and Smart TV devices.

As part of the latest game broadcast rights for Asia Cup, Sony LIV built a streaming analytics solution using AWS services that successfully processed millions of concurrent sessions in real-time.

## The challenge of batch processing

As Sony LIV’s audience grew and live sports events attracted increasingly large viewership, the team identified an opportunity to move from batch-based analytics to a real-time data application. The existing architecture processed data reliably in scheduled batches, but the growing scale of live events called for faster, more granular insights. The team set out to address three key areas:

1. **Real-Time Visibility:** Track frontend user events, journeys, and conversion funnels in near real-time, especially during high-stakes live sports streams, to see peak concurrent viewership and respond to engagement patterns as they happen.
2. **Comprehensive Quality Monitoring:** Implement end-to-end monitoring of video quality key performance indicators (KPIs) including buffering rates, playback failures, video start time, and rebuffering events to proactively enhance the viewer experience.
3. **Unified Data Architecture:** Consolidate data from multiple sources into a unified architecture to enable comprehensive customer views, supporting future personalization and machine learning (ML)-driven recommendations.

Sony LIV needed to evolve from reactive batch processing to a real-time data application to deliver actionable engagement insights at scale and establish the foundation for unified customer profiles.

## Streaming analytics architecture

![Streaming analytics architecture showing data from mobile, web, and Smart TV apps flowing through Amazon EKS into real-time and batch processing paths on AWS](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2026/08/26/BDB-5907-1.png)

Figure 1: Sony LIV streaming analytics architecture on AWS

Data from mobile, web, and Smart TV applications flows through Application Load Balancers to [Amazon Elastic Kubernetes Service](https://aws.amazon.com/eks/) (Amazon EKS) pods for validation and preprocessing. The architecture implements parallel processing paths to balance speed and cost efficiency.

**Real Time Path:** Priority events requiring immediate action such as playback failures, user interactions, and live sports engagement signals stream through [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) for sub-second processing. These events flow directly to ClickHouse using the ClickHouse connector, enabling real-time analytics with minimal latency.

**Batch Path:** High-volume batch events are ingested via [Amazon Data Firehose](https://aws.amazon.com/firehose/) into a raw landing zone on [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/), partitioned by event type and time. [Amazon EMR](https://aws.amazon.com/emr/) running Apache Spark then processes this raw data performing schema validation, deduplication, and transformations — and writes the curated output as [Apache Iceberg](https://iceberg.apache.org/) tables back to S3

**Unified Data Layer:** AWS Glue catalogs data across streaming and batch sources, creating a unified schema that powers the customer data application. This unified data layer serves as the foundation for building comprehensive customer profiles and enabling personalized recommendations.

**Analytics and Monitoring:** ClickHouse serves as the low-latency analytics engine, powering real-time dashboards and video quality monitoring. Operations teams track critical KPIs including peak concurrent viewership, buffering rates, video start time, and playback failures, enabling rapid response to issues during live events.

Custom dashboards and Datadog provide visualization for business metrics and application performance monitoring, while Amazon CloudWatch tracks infrastructure health, delivering end-to-end visibility across the application.

## Results and business impact

**The results:** product, analytics and engineering teams now operate from a single unified dashboard, making real-time decisions with data that is seconds, not hours old. Auto scaling and serverless design have optimized costs while providing reliability at peak load. At the foundation, a centralized data catalog now serves as a single source of truth for business intelligence, machine learning workloads and operational monitoring.

The transformation helped Sony LIV process millions of concurrent sessions in real time, particularly during high-profile events such as the Asia Cup 2025.

1. **Accelerated insights**: Data latency dropped from hours to seconds, enabling instant insights into viewer behavior, content performance, and streaming health.
2. **Unified decision-making**: Product, analytics, and engineering teams now use unified dashboards for real-time decision-making.
3. **Optimized operations**: The solution auto scaling and serverless design optimized costs while providing reliability and fault tolerance.

Beyond performance gains, the new architecture established a strong foundation for personalized content recommendation and operational agility. By integrating a centralized data catalog and scalable analytics layer, the solution now provides a single source of truth for business intelligence, machine learning workloads, and monitoring.

## Future innovations

Sony LIV plans to expand its analytics capabilities by integrating advanced ML models for real-time recommendations, user churn prediction, and anomaly detection. The team will also focus on building unified customer profiles to enable hyper-personalized experiences.

The AWS based architecture provides a strong foundation for future growth and innovation, enabling Sony LIV to deliver highly personalized experiences to an expanding viewer base.

## Conclusion

By adopting AWS, Sony LIV transformed its analytics architecture into a real-time, scalable, and insight-driven solution. The solution reduced data latency from hours to seconds, enabled processing of millions of concurrent sessions during peak events, and positioned Sony LIV as a leader in streaming analytics innovation in India.

To learn more about how AWS can help your media organization implement real-time streaming analytics solutions, explore the following resources:

- [AWS for Media & Entertainment](https://aws.amazon.com/media/) – Discover how AWS powers content delivery, streaming, and analytics for media companies worldwide.
- [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/) – Learn about the fully managed service for real-time data streaming used in this solution.
- [Data Streaming Analytics on AWS (AWS Blog)](https://aws.amazon.com/blogs/media/category/analytics/) – Read related posts on how customers are building streaming analytics pipelines on AWS.

* * *

## About the authors

### Resources

- [Amazon Athena](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-athena?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon EMR](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-emr?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon Kinesis](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-kinesis?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon MSK](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-managed-streaming-for-apache-kafka/)
- [Amazon QuickSight](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-quicksight?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [Amazon Redshift](https://aws.amazon.com/blogs/big-data/category/analytics/amazon-redshift-analytics?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)
- [AWS Glue](https://aws.amazon.com/blogs/big-data/category/analytics/aws-glue?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-resources)

* * *

### Follow

- [Twitter](https://twitter.com/awscloud)
- [Facebook](https://www.facebook.com/amazonwebservices)
- [LinkedIn](https://www.linkedin.com/company/amazon-web-services/)
- [Twitch](https://www.twitch.tv/aws)
- [Email Updates](https://pages.awscloud.com/communication-preferences?sc_ichandle=ha&sc_icampaign=acq_awsblogsb&sc_icontent=bigdata-social)