# BigQuery Utils

## config_util.py

#### BqConfig

Sample config.yml file:
```
---
table_name:  # name of table in BigQuery
description:  # optional table description
dataset_name:  # name of dataset in BigQuery 
column_mapper:  # map source column names to dataset column names 
  - Column One: column_one
    Column-Two: column_two
type_conversions:  # any necessary type conversions before loading to bigquery
  - name: # name of mapped column (eg. column_name instead of Column Name)
    type:  # python datatype -- (str,int,float,bool,datetime,...)
    formatter:  # format string incase of datetime parsing
schema:  # BigQuery schema
  - name:  # mapped column name
    field_type:  # BigQuery datatype:
                    # NUMERIC (INT65, NUMERIC, BIGNUMERIC, FLOAD64)
                    # BOOLEAN
                    # STRING
                    # BYTES
                    # TIME (DATE, TIME, DATETIME, TIMESTAMP)
                    # GEOGRAPHY
                    # ARRAY
                    # STRUCT
    mode:  # BigQuery column mode -- (Nullable,Required,Repeated)
    description:  # (optional) column description
time_partitioning:  # (optional) if table is time partitioned 
  - field:  # name of column on which table is partitioned
    type:  # time-unit of partition -- (HOUR,DAY,MONTH,YEAR)
```