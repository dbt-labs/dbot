# dbt CLI Commands Cheatsheet

## Run a model

The following command is how to select and run a specific model.

```
dbt run --select model
```

## Run a model and all its children downstream

The following command is how to select and run a specific model and all of its children.

```
dbt run --select model+
```

## Run a model and all its parents upstream

The following command is how to select and run a specific model and all of its parents.

```
dbt run --select +model
```

## Run a model and its direct parents upstream

The following command is how to select and run a specific model and one layer of its immediate parents. Changing the 1 to a 2 would run 2 layers deep, the model and all the models up through its parents’ parents, and so on.

```
dbt run --select 1+model
```

## Run a model and its direct children downstream

The following command is how to select and run a specific model and one layer of its immediate children. Changing the 1 to a 2 would run 2 layers deep, the model and all the models down through its children’s children, and so on.

```
dbt run --select model+1
```

## Run a model, its upstream parents, and one layer of its direct children downstream

The following command is how to select and run a specific model, all of its upstream parents, and one layer of its immediate children. Changing the 1 to a 2 would run 2 layers deep, the model and all the models down through its children’s children, and so on.

```
dbt run --select +model+1
```

## Run a specific snapshot

The following command is how to select and run a specific snapshot.

```
dbt snapshot --select model
```

## Incremental model full refresh

Here’s how to rebuild an incremental from scratch.

```
dbt build --select model --full-refresh
```

## Run all the models

The following command is how to run all the models in your dbt project.

```
dbt run
```

## The difference between run and build

The command `build` combines multiple commands, it executes `run` and `test` for each model selected instead of running all the models and then testing all the models. If a run or test fails for a model it skips all of its downstream dependencies. This way you don’t build anything on faulty models or waste resources building things that later fail tests.

## Build all the models

```
dbt build
```

## List all the available models

The following command is how to list all the available models in your dbt project.

```
dbt ls
```

## Compile SQL from dbt project

The following command is how to compile the SQL from your dbt project without running it.

```
dbt compile
```

## Test your models

The following command is how to run all your tests.

```
dbt test
```

## Test a model and all its parents upstream

The following command is how to select and test a specific model and all of its parents.

```
dbt run --select +model
```

## Test a model and its direct parents upstream

The following command is how to select and test a specific model and one layer of its immediate parents. Changing the 1 to a 2 would run 2 layers deep, the model and all the models up through its parents’ parents, and so on.

```
dbt run --select 1+model
```

## Test a model and its direct children downstream

The following command is how to select and run a specific model and one layer of its immediate children. Changing the 1 to a 2 would run 2 layers deep, the model and all the models down through its children’s children, and so on.

```
dbt run --select model+1
```

## Test all your models’ source freshness

```
dbt source freshness
```

## Test a specific model’s source freshness

```
dbt source freshness --select model
```

## Test the source freshness of a model and all its parents upstream

```
dbt source freshness --select +model
```

## Test the source freshness of a model and all its children downstream

```
dbt source freshness --select model+
```

## Test the source freshness of a model and its direct parents upstream

The following command is how to select and test the source freshness of a specific model and one layer of its immediate children. Changing the 1 to a 2 would run 2 layers deep, the model and all the models down through its children’s children, and so on.

```
dbt source freshness --select 1+model
```

## Test the source freshness of a model and its direct children downstream

The following command is how to select and test the source freshness of a specific model and one layer of its immediate children. Changing the 1 to a 2 would run 2 layers deep, the model and all the models down through its children’s children, and so on.

```
dbt source freshness --select model+1
```

## `dbt_project.yml` Project YAML Config with comments

The following is an example of the `dbt_project.yml` YAML config file with project-level configuration for a dbt project.

```
# the name of the project
name: string

config-version: 2
version: version

# the profile to use from the `profiles.yml`
profile: profilename

# the following settings let you overwrite the default configs for where dbt
# should look for certain objects

# the directory to look for models in
model-paths: [directory path]

# the directory to look for seeds in
seed-paths: [directory path]

# the directory to look for custom tests in
test-paths: [directory path]

# the directory to look for analyses in
analysis-paths: [directory path]

# the directory to look for project-scoped macros in
macro-paths: [directory path]

# the directory to look for snapshots in
snapshot-paths: [directorypath]

# the directory to look for docs blocks in
docs-paths: [directory path]

# the directory to look for static assets like images in,
# for dbt docs
asset-paths: [directory path]

# the directory to build into
target-path: [directory path]

# the directory to save logs into
log-path: [directory path]

# the directory to save packages into when `dbt deps` is run
packages-install-path: [directory path]

# set a list of directories for dbt to clean when `dbt clean` is run,
# by default this `packages` and `target`.
clean-targets: [directorypath]

query-comment: string

# set a required version or range of versions for dbt,
# in order for this project to run properly
require-dbt-version: version-range | [version-range]

quoting:
  database: true | false
  schema: true | false
  identifier: true | false

# set directory level configurations for models
models:
  <model-configs>

# set directory level configurations for seeds
seeds:
  <seed-configs>

# set directory level configurations for snapshots
snapshots:
  <snapshot-configs>

# set directory level configurations for sources
sources:
  <source-configs>

# set directory level configurations for tests
tests:
  <test-configs>

# set global variables for the project
vars:
  <variables>

# set a hook to run when a dbt run starts
on-run-start: sql-statement | [sql-statement]

# set a hook to run when a dbt run finishes
on-run-end: sql-statement | [sql-statement]

dispatch:
  - macro_namespace: packagename
    search_order: [packagename]
```
