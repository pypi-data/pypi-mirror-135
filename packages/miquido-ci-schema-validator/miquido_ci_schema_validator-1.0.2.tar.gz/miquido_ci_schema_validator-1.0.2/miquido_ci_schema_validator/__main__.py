from miquido_ci_schema_validator import validate_yml

if __name__ == '__main__':
    with open('.miquido-ci.yml', 'r') as f:
        validate_yml(f.read())
