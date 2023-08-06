# DBTonFHIR

## Description

<!-- Describe the feature and how it solves the problem. -->

The goal is to be able to map from a given source to a FHIR server without the help of a gui leveraging existing tools
such as git and DBT.

## Project template repository

[dbtonfhir-template](https://github.com/arkhn/dbtonfhir-template)

## Setup and installation

### Prerequisites
- Python 3.9+

### Base setup

- Create an `.env` file and specify your own configuration (you can copy `.env.template` 
and customize)

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements/tests.txt
pre-commit install 
```

### IntelliJ/Pycharm setup

Install the [ProjectEnv](https://plugins.jetbrains.com/plugin/17044-projectenv) plugin to load
environment variables from your `.env` file

## Fhir Cli

### Install

```shell
make install 
```

### Build package

```shell
make build
```

### Usage

```shell
fhir --help
```

<img width="605" alt="Screenshot 2022-01-06 at 16 44 19" src="https://user-images.githubusercontent.com/34629112/148412894-3fe93879-1ee1-4f12-8f1d-df97ddb69a0d.png">

## OMOP

### Vocabulary

- Download vocabularies at https://athena.ohdsi.org/
- Create a `vocabulary` folder and extract the files there

### CDM 5.4

To build the OMOP CDM 5.4 schema in your target database, execute the following files in this order:

1. `OMOPCDM_postgresql_5.4_ddl.sql`
2. `OMOPCDM_postgresql_5.4_primary_keys.sql`
3. `vocabulary.sql`
4. `OMOPCDM_postgresql_5.4_constraints.sql`
5. `OMOPCDM_postgresql_5.4_indices.sql`

## Tests

### Unit tests
```shell
make unit-tests
```
### End to end tests
```shell
make e2e-tests
```

## Versioning and publishing
This project follows the [semver](https://semver.org/) versioning.

To bump the version, edit the `version` attribute in `setup.cfg` and add a tag on the `main` branch
with the version prefixed with a `v` (eg. `v0.1.0`). Be careful to tag with the same version
specified in `setup.cfg`.

```shell
git tag v0.1.0
git push --tags
```

As soon as the tag is pushed, a package will be built and published to Pypi.

## References

### Debezium

This project uses the [Debezium](https://debezium.io/documentation/reference/stable/architecture.html) framework for extract-load tasks

### Kafka Connect

* [JDBC Connector documentation](https://docs.confluent.io/kafka-connect-jdbc/current/)

## Implementation

![arkhn](https://user-images.githubusercontent.com/34629112/143152402-6b2522b2-7cd3-4fc5-8843-381a723ea3d8.jpg)
