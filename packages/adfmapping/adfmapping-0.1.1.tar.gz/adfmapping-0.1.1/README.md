# adfmapping
ADF Dynamic mapping of Source Data/columns to Sink Columns.
---
### Pre-requisites
Both tech and non-tech audiences can use it with a lil bit of guidance.

-  [Python 3+ installed](https://www.python.org/downloads/)  on your machine

### Usage
-  Get Csv file from your Azure Application Insights or Log Analytics workspace

![APPIN_QUERY_Example.png](APPIN_QUERY_Example.png)

- Install the package 
    > pip install adfmapping

- Run the below command to generate mapping JSON.  
    > adfmapping Mapping --csvfile C:\user\appIn.csv