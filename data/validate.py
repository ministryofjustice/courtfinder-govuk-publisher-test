import jsonschema
import json


with open('court-schema.json', 'r') as schema_file:
    schema = json.loads(schema_file.read())
    with open('sample_court.json', 'r') as court_file:
        court = json.loads(court_file.read())
        print not jsonschema.validate(court, schema)

        
