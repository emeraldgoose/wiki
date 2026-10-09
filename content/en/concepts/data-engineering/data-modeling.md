---
title: Data Modeling for Analytics
description: Star and snowflake schemas, normalization vs denormalization, slowly changing dimensions, examples, pitfalls, and references
tags: [concept, data-engineering, data-modeling, analytics, schema]
locale: en
published: 2026-09-07
---

# Data Modeling for Analytics

**Data modeling** organizes business data into structured formats that support analytical querying and reporting. The choice of schema design directly impacts query performance, data maintainability, and storage efficiency.

## Star Schema

A **star schema** consists of a single large fact table surrounded by dimension tables. The fact table contains foreign keys referencing dimension tables and measurable metrics (e.g., sales amount, transaction count). Dimensions are denormalized, holding attributes descriptive of the foreign key (e.g., `product_name`, `customer_city`). See also `[[apache-spark|Spark]]` and `[[dbt|data build tool]]` for common star schema implementations.

### Advantages

- Simple query patterns: star joins are intuitive and the query optimizer can easily cardinality-estimate.
- Fewer joins required compared to normalized schemas.
- Aggressive denormalization is acceptable because dimension tables are typically small and read-heavy.

### Disadvantages

- Dimension tables contain redundant data, leading to larger storage footprints.
- Updates to dimension attributes require careful handling (e.g., slowly changing dimensions).

### Example

```sql
-- Fact table
CREATE TABLE sales (
  sale_id BIGINT,
  product_key INT,
  customer_key INT,
  store_key INT,
  sale_date DATE,
  amount DECIMAL(10,2),
  quantity INT
);

-- Dimension tables (denormalized)
CREATE TABLE products (
  product_key INT PRIMARY KEY,
  product_name VARCHAR(100),
  category VARCHAR(50),
  subcategory VARCHAR(50),
  brand VARCHAR(50)
);

CREATE TABLE customers (
  customer_key INT PRIMARY KEY,
  customer_name VARCHAR(100),
  segment VARCHAR(20),
  city VARCHAR(50),
  country VARCHAR(50)
);
```

## Snowflake Schema

A **snowflake schema** normalizes dimension tables further, breaking them into multiple related tables. While the fact table remains unchanged, dimensions are split into sub-tables linked by foreign keys, forming a snowflake-like shape. Compare with `[[snowflake-schema|snowflake schema]]` organization (normalized).

### Advantages

- Reduced storage redundancy versus star schema.
- Easier maintenance: changes to one sub-table propagate without affecting the entire dimension.

### Disadvantages

- More joins required per query, which can increase latency.
- Query complexity rises; the optimizer must navigate additional foreign key paths.
- Benefit diminishes when dimension sub-tables are small; star schema is usually preferred.

### Example

```sql
-- Fact table (same as star schema)
CREATE TABLE sales (...);

-- Normalized product hierarchy
CREATE TABLE categories (
  category_key INT PRIMARY KEY,
  category_name VARCHAR(50)
);

CREATE TABLE subcategories (
  subcategory_key INT PRIMARY KEY,
  subcategory_name VARCHAR(50),
  category_key INT,
  FOREIGN KEY (category_key) REFERENCES categories(category_key)
);

CREATE TABLE products (
  product_key INT PRIMARY KEY,
  product_name VARCHAR(100),
  subcategory_key INT,
  FOREIGN KEY (subcategory_key) REFERENCES subcategories(subcategory_key)
);
```

## Normalization vs Denormalization

| Aspect | Normalized | Denormalized |
|--------|-----------|--------------|
| **Structure** | Multiple tables, 3NF or higher | Fewer tables, repeated attributes |
| **Storage** | Minimal redundancy | Higher storage due to duplication |
| **Write workload** | Efficient: single-table updates | Costlier: updates across copies |
| **Read workload** | More joins, potentially slower | Fewer joins, faster analytical queries |
| **Typical use** | Operational OLTP systems | Analytical OLAP / data warehouse |

The general rule for analytics: **denormalize aggressively** for read performance, accepting storage cost. Normalize only when write integrity or dimensional maintainability is the priority.

## Slowly Changing Dimensions (SCD)

Dimensions in a data warehouse rarely stay static. **Slowly Changing Dimensions** capture gradual changes without losing historical integrity.

| SCD Type | Behavior | SQL Pattern |
|----------|----------|-------------|
| **Type 1** | Overwrite existing value; no history kept | `UPDATE dim SET city = 'NewYork' WHERE key = 1` |
| **Type 2** | Add new row with effective/end dates; full history kept | `INSERT INTO dim VALUES (1, 'NewYork', '2024-01-01', '9999-12-31')` |
| **Type 3** | Store previous value in a separate column; limited history | `UPDATE dim SET old_city = city, city = 'NewYork' WHERE key = 1` |

**Type 2** is the most common in analytical warehouses; it enables time travel queries and trend analysis. The pattern requires `effective_from` and `effective_to` (or `is_current`) columns on every dimension table using SCD.

### Example: Type 2 SCD

```sql
CREATE TABLE customers (
  customer_key INT,
  customer_name VARCHAR(100),
  city VARCHAR(50),
  country VARCHAR(50),
  effective_from DATE,
  effective_to DATE,
  is_current BOOLEAN DEFAULT TRUE
);

-- Insert new row when city changes
INSERT INTO customers (customer_key, customer_name, city, country, effective_from, effective_to, is_current)
VALUES (1, 'Alice', 'NewYork', 'USA', '2024-01-01', '9999-12-31', TRUE);

-- Future update: mark old row, insert new
UPDATE customers SET is_current = FALSE WHERE customer_key = 1 AND is_current = TRUE;
INSERT INTO customers (customer_key, customer_name, city, country, effective_from, effective_to, is_current)
VALUES (1, 'Alice', 'Boston', 'USA', '2024-06-01', '9999-12-31', FALSE);
```
