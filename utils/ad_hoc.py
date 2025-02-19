import json
from pathlib import Path

import duckdb

# Read and parse the JSON file
json_path = Path("src/data/output/drug_mentions.json")
if not json_path.exists():
    raise FileNotFoundError(f"{json_path.resolve()} not found.")

# Parse JSON and load it
json_data = json.loads(json_path.read_text(encoding="utf-8"))
json_literal = json.dumps(json_data)

con = duckdb.connect()

# create a table with the JSON data
con.execute(
    f"""
    CREATE OR REPLACE TABLE dm AS 
    WITH j AS (
      SELECT CAST('{json_literal}' AS JSON) AS js
    )
    SELECT 
        key AS drug,
        json_extract(js, '$.' || key || '.mentions.journals') AS journals
    FROM j,
    UNNEST(json_keys(js)) AS t(key)
    WHERE key != '';
"""
)

# Count distinct drugs per journal with better handling of journal names
con.execute(
    """
    WITH RECURSIVE journal_mentions AS (
        SELECT 
            drug,
            TRIM(BOTH '"' FROM UNNEST(json_extract(journals, '$[*].name')::VARCHAR[])) AS journal_name
        FROM dm
        WHERE journals IS NOT NULL
    )
    SELECT 
        journal_name,
        COUNT(DISTINCT drug) AS distinct_drugs,
        GROUP_CONCAT(DISTINCT drug) AS drugs_list
    FROM journal_mentions
    WHERE journal_name != ''
      AND journal_name NOT LIKE '%\\\\%'  -- Exclude malformed journal names
    GROUP BY journal_name
    ORDER BY distinct_drugs DESC
    LIMIT 1;
"""
)

result = con.fetchall()
if result:
    print(
        f"Le journal qui mentionne le plus de médicaments différents est {result[0][0]} "
        f"avec {result[0][1]} médicaments différents : {result[0][2]}"
    )
