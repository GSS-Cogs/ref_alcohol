#!/bin/env python3

from csv import DictReader
from gssutils import pathify
import uritemplate
import json

column_titles = {}
columns_names = set()
with open('columns.csv') as columns_file:
    for row in DictReader(columns_file):
        column_titles[row['title']] = row
        columns_names.add(row['name'])

for col in column_titles.values():
    if col['value_template'] != '':
        vars = set(uritemplate.variables(col['value_template']))
        assert vars.issubset(columns_names)

codelists_metadata = json.load(open('codelists-metadata.json'))
codelists = [(table['url'], table['rdfs:label']) for table in codelists_metadata['tables']]
codelist_uris = [f"http://gss-data.org.uk/def/concept-scheme/{pathify(label)}" for (file, label) in codelists]

component_labels = {}
with open('components.csv') as components_file:
    for row in DictReader(components_file):
        component_labels[row['Label']] = row
        if row['Component Type'] == 'Measure':
            assert row['Label'] in column_titles.keys(), f"Measure '{row['Label']}' should be listed in columns.csv."
            column_spec = column_titles[row['Label']]
            assert column_spec['component_attachment'] == 'qb:measure'
            assert column_spec['property_template'] == f"http://gss-data.org.uk/def/measure/{pathify(row['Label'])}", f"Property templates are different, {column_spec['property_template']} should be http://gss-data.org.uk/def/measure/{pathify(row['Label'])}"
        elif row['Component Type'] == 'Dimension':
            assert row['Label'] in column_titles.keys()
            column_spec = column_titles[row['Label']]
            assert column_spec['component_attachment'] == 'qb:dimension'
            if column_spec['property_template'].startswith('http://gss-data.org.uk/'):
                assert column_spec['property_template'] == f"http://gss-data.org.uk/def/dimension/{pathify(row['Label'])}", f"property_template mismatch '{column_spec['property_template']}' != 'http://gss-data.org.uk/def/dimension/{pathify(row['Label'])}'"
            if row['Codelist'].startswith('http://gss-data.org.uk/'):
                assert row['Codelist'] in codelist_uris, f"Codelist '{row['Codelist']}' not defined in codelists-metadata.json"
            if column_spec['value_template'].startswith('http://gss-data.org.uk'):
                assert column_spec['value_template'].startswith(f"http://gss-data.org.uk/def/concept/{pathify(row['Label'])}/"), f"Expecting value_template to look like 'http://gss-data.org.uk/def/concept/{pathify(row['Label'])}'"
        elif row['Component Type'] == 'Attribute':
            assert row['Label'] in column_titles.keys()
            column_spec = column_titles[row['Label']]
            assert column_spec['component_attachment'] == 'qb:attribute'
            if column_spec['property_template'].startswith('http://gss-data.org.uk/'):
                assert column_spec['property_template'] == f"http://gss-data.org.uk/def/attribute/{pathify(row['Label'])}"
