# fondat-core

[![PyPI](https://img.shields.io/pypi/v/fondat-core)](https://pypi.org/project/fondat-core/)
[![Python](https://img.shields.io/pypi/pyversions/fondat-core)](https://python.org/)
[![GitHub](https://img.shields.io/badge/github-main-blue.svg)](https://github.com/fondat/fondat-core/)
[![Test](https://github.com/fondat/fondat-core/workflows/test/badge.svg)](https://github.com/fondat/fondat-core/actions?query=workflow/test)
[![License](https://img.shields.io/github/license/fondat/fondat-core.svg)](https://github.com/fondat/fondat-core/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

A foundation for Python resource-oriented applications. 

## Introduction

Fondat is a foundation for building resource-oriented applications in Python.
By composing your application as a set of resources that expose operations,
they can be automatically exposed through an HTTP API.

## Features

* Asynchronous uniform resource interface.
* Resource operations can be exposed through HTTP API.
* Type encoding and validation of resource operation parameters and return values.
* Authorization to resource operations enforced through security policies.
* Abstraction of SQL tables, indexes and queries.
* Monitoring of resource operations and elapsed time in time series databases.
* Generates [OpenAPI](https://www.openapis.org/) documents, compatible with [Swagger UI](https://swagger.io/tools/swagger-ui/).

## Install

```
pip install fondat-core
```

## Develop

```
poetry install
poetry run pre-commit install
```

## Test

```
poetry run pytest
```
