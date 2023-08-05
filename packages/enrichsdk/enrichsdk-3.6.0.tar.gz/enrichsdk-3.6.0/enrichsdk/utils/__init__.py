from sqllineage.runner import LineageRunner

from .sample import *

def get_lineage_of_query(engine, sql):
    """
    Given an engine and an SQL expression, find the input
    and output tables. Replace <default> with database 
    name from the engine
    """
    dependencies = []
    result = LineageRunner(sql, verbose=True)

    database = engine.url.database

    # Get input tables..
    if len(result.source_tables) > 0:
        tables =[str(t).replace("<default>",database) for t in result.source_tables]

        tables = {
            t.split(".")[-1] : {
                'text': t.replace(".", " "),
                'table': t
            } for t in tables
        }
        dependencies.append({
            "type": "db",
            "nature": "input",
            "objects": tables,
        })

    # Get output dependencies
    if len(result.target_tables) > 0:
        tables =[str(t).replace("<default>",database) for t in result.target_tables]
        tables = {
            t.split(".")[-1] : {
                'text': t.replace(".", " "),
                'table': t
            } for t in tables
        }

        dependencies.append({
            "type": "db",
            "nature": "output",
            "objects": tables
        })

    return dependencies

