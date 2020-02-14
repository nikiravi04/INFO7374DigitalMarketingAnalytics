## Marketa Analytics Dashboard

Started in 1999, Alibaba.com is the leading platform for global wholesale trade. We serve millions of buyers and suppliers around the world.

### What are we doing for Marketa?

*What?*

Illustrate the value of data driven analytics with the following themes to be included 
Pricing 
Promotion 
Search 
Recommendations 

*Where?*

Marketa wants you to analyze the data using tools (Pandas, xsv, Trifacta) and build a dashboard using Einstein analytics

*Why?*

- To work with datasets using Pandas, xsv(xcsv) and Trifacta tools 
- To be able to analyze marketing data using Salesforce Einstein analytics studio 
- Derive insights from the datasets 
- Crisply communicate and document your findings

*How*

- Firstly, we had .txt files which had to be converted to .csv files using Pandas
- As there were only 30 rows in our dataset, we had to generate fake data to accomplish data driven analytics using the python package Faker
- Accomplished joining of 15 tables using XSV tool to combine them into two main tables 'User' and 'Vendor'
- Exploratory Data Analysis done to find out the Big Spender and Many Orders in pandas
- Cleaned the data using Trifacto (null values, splitting the columns, filtering data)
- The cleaned dataset was imported to Salesforce Einstein Analytics and joined to create a dataflow
- Dashboards were created using Einstein Analytics for
  - Sales Insights
  - Time series for predicting the sales
  - Email Target marketing 
