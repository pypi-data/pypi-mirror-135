We attempt to follow semantic versioning for this tool.

> We started tracking Release Notes as of version 3.0.0.

## 4.0.2

* `parse ansible json` CLI endpoint can now parse Ansible *loop* results (recursively).

## 4.0.1

* Fix Python 3.6 support.

## 4.0.0

> Yanked from PyPI due to continued Python 3.6 incompatibility.

* Added support for Python 3.6
* Adding release notes and improve `docs/`. 
* **Backwards incompatible change:** Removed buggy '--tail' argument and code from `post teams card` CLI endpoint.
    * Replaced '--tail' with '--trim'
    * 'trim' cuts off the end of the message instead of the beginning.

## 3.0.2

* Fixed Source Distribution, to include all `docs/` and other required dependencies.
* Rewrite of the CLI framework.
* Rewrite of 'Parsing Ansible JSON' modules/packages, to capture more error messages successfully. 
* Added `--crucial-task` and `--crucial-task-type` filter parameters to `parse ansible json`.
* Addition of `docs/` directory (driven via mkdocs).

## 3.0.1

> Yanked from PyPI due to Broken Source Distribution.

## 3.0.0

> Yanked from PyPI due to Broken Source Distribution.
