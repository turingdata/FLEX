 # Task 2. Data Validation 
Create an entity relationship diagram (ERD) that represents the structure for the balance sheet 
data provided in the JSON file attached.

### In your terminal CD into the project folder

### Set up virtual environment in the project folder

    `python -m venv .venv`

Activate the environment: 

For Linux/MacOS:

    `source .ven/bin/activate` 

For Windows:

    `.venv/Scripts/Activate.ps1` 

### Install dependencies

    `pip install -r requirements.txt`

### Run Your Validation Python Scripts

    `python ./Scripts/validator.py`

### Review the Outputs folder for discrepancies and validation logs
    ex: 
    `
    2025-03-27 00:17:24,134 - INFO - Successfully loaded JSON file: data/financial_data.json
    2025-03-27 00:17:24,134 - INFO - Validating Assets section
    2025-03-27 00:17:24,134 - INFO - Validating Liabilities section
    2025-03-27 00:17:24,134 - WARNING - Discrepancy found for 'Current Liabilities' (Parent: 'Liabilities')
    2025-03-27 00:17:24,134 - INFO - Validating Equity section
    2025-03-27 00:17:24,134 - INFO - Roll-up validation completed successfully. Report saved as 'rollup_discrepancy_report.txt'.
    2025-03-27 00:18:24,082 - ERROR - Error decoding JSON file data/financial_data.json: Invalid control character at: line 18 column 71 (char 1323)
    2025-03-27 00:18:24,084 - ERROR - Validation failed: Invalid control character at: line 18 column 71 (char 1323)
    `


## General Approach

My approach started with understanding the structure and hierarchy of the provided JSON file. 
Since the data was deeply nested, I first focused on identifying parent-child relationships and how financial categories (**Assets, Liabilities, Equity**) were organized.

To better work with and visualize the data, I used Visual Studio Code. I relied on JSON formatting extensions such as:

**Prettify JSON** 

Once I understood the hierarchical structure of the JSON data, I focused on designing an Entity-Relationship Diagram (ERD) that reflects the parent-child nesting of financial accounts in Task1 (`See Task1_ERD.md`)


## Assumptions

- Not all items had an **account_id,** so I assumed those were grouping nodes,
and represents a collection of sub-items. Thus I generated **unique ID**s (or incremental integers) to maintain the parent-child structure.


- Roll-up validation logic assumed that a parent’s value should equal the sum of its children, allowing for a small **float tolerance of ±0.01** to account for decimal precision.

- Since the data was provided as a static JSON, I assumed no real-time updates or transactional context were needed (e.g., no deltas or timestamps).


## Issues or Inconsistencies Found in the Dat
- The json file was unvalid. In two line the space should be deleted.

- The structure is recursive, but no explicit parent_id is given in the original data — this had to be inferred from nesting.

## Future_Work / What I Would Do Next With More Time
- I can improve  `parse_jason.py` script that flattened the nested JSON structure into a DataFrame that includes id, name, value, and parent_id. I would improve logging, error handling, reporting and visualizations.
Especially if automated this, I'd add emailing, slack notifications etc.. if process failed.

- I can extend the validation logic to check for empty groups, duplicate names, or anomalies in value flow.
    Here some of the features I would add:
        Missing or Null Values:
        	Ensures critical fields are not missing or null. Causes common non-divisible by zero error in analytics. Better to handle these upstream than downstream.
        Negative Values :
        	Certain fields  won't have negative values.	I'd avoid unrealistic financial data.
        Data Type Validation:
        	Ensures fields are of the correct data type (numeric values for financial fields)	Prevents incorrect data processing
        Range Validotion:
        	Ensures values are within acceptable thresholds (e.g., asset values are not below zero)	Preventing outlier errors
        Circular Reference Detection:
        	Detects circular references in hierarchical data (parent-child cycles)	to prevent infinite loops
        Consistency Check:
        	Ensures consistency between relatd nodes in different sections (e.g., assets and liabilities)
        Historical Data Validation:
        	Validates the growth or consistency of financial data over time (e.g., retained earnings)

- I used a hardcoded list of top-level categories ("assets", "liabilities", and "equity"). With more time, I could add logic to dynamically detect and analyze the first-level parent groupings instead of relying on predefined values.

- I would build a containerized  (ex. Docker) pipeline that would ingest the data (modeling API connectivity with fivetran or Airbyte), transform the data (modeling lambdas or Glue), build a datawarehouse using DBT , add visualization using opensource tools such as Plotly Dash or Grafana (modeling premium solutions such as Looker or Tableau) . 
See:
    `Future_Work/docker-compose.yml`
