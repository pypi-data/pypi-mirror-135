# sqlcli

A command line interface (CLI) for interacting with SQLModel.

<hr>

**Source code:** [https://github.com/SamEdwardes/sqlcli](https://github.com/SamEdwardes/sqlcli)

**Docs:** [https://samedwardes.github.io/sqlcli/](https://samedwardes.github.io/sqlcli/)

**PyPi:** *not yet published*

<hr>

## Installation

You can install *sqlcli* using pip:

```bash
pip install sqlcli
```

This will make the `sqlcli` command available in your python environment.

## Usage

The quickest way to get started with *sqlcli* is to create a demo sqlite database:

```bash
sqlcli init-demo
```

This will create a small sqlite database on your computer. The you can use sqlcli to explore your database.

```bash
sqlcli select athlete --database-url "sqlite:///demo_database.db" --models-module "demo_models.py"
```
