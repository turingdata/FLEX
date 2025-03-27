 # Task 2. Data Validation 
Create an entity relationship diagram (ERD) that represents the structure for the balance sheet 
data provided in the JSON file attached.

## In your terminal CD into the project folder

## Set up virtual environment in the project folder

    `python -m venv .venv`

Activate the environment: 

For Linux/MacOS:

    `source .ven/bin/activate` 

For Windows:

    `.venv/Scripts/Activate.ps1` 

## Install dependencies

    `pip install -r requirements.txt`

#### Run Your Python Script

    `python ./utilities/rollup_validation.py`


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

## What I Would Do Next With More Time
- I can improve  `parse_jason.py` script that flattened the nested JSON structure into a DataFrame that includes id, name, value, and parent_id. I would add logging, error handling, reporting and visualizations.

- I can extend the validation logic to check for empty groups, duplicate names, or anomalies in value flow.

- I used a hardcoded list of top-level categories ("assets", "liabilities", and "equity"). With more time, I could add logic to dynamically detect and analyze the first-level parent groupings instead of relying on predefined values.

- I would build a containerized  (ex. Docker) pipeline that would ingest the data (modeling API connectivity with fivetran or Airbyte), transform the data (modeling lambdas or Glue), build a datawarehouse using DBT , add visualization using opensource tools such as Plotly Dash or Grafana (modeling premium solutions such as Looker or Tableau) . 