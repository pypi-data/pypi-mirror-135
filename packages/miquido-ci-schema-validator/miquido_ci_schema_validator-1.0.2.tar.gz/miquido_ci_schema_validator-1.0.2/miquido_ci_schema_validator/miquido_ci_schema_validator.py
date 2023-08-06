from jsonschema import validate
import requests
import yaml


def validate_yml(yml):
    schema = requests.get('https://schema.miquido.dev', timeout=30).text
    validate(yaml.safe_load(yml), yaml.safe_load(schema))
