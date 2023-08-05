# Changelog
Here you will find a changelog of all the SDK releases.


## [6.0.1] 2022-01-17
This release has breaking changes
- Change Task api to Model.
  1. superwise.task -> superwise.model
  2. task_id fields changed to model_id


## [5.3.5] 2022-01-06
- Bug fix - log transaction path


## [5.3.4] 2021-12-23
- Better error handling, remove code duplications in _check_res and parse_response functions
- Imrprove docstrings

## [5.3.1] 2021-12-22
- Changed requirments.txt file to have better and more flexible versioning.
- Improve docstrings for better API documentation


## [5.2.15] 2021-12-22
This release does not have any breaking changes.
This release optimize the transaction log from s3 method


## [5.2.0] 2021-12-14
This release has breaking changes
- added get_by_name support for task and version
- Changed DataEntityRole enum to DataTypesRoles
- support for suppling DataEntityRole as enum object
-
- few bug fixes and small improvements
- improve docstrings

## [5.1.1] 2021-12-14
Added support for infer dtypes

## [5.0.3] 2021-12-14
This release does not have any breaking changes.
This release adds an SDK reference guide to our SDK.

## [5.0.1] 2021-12-01
This release has breaking changes - change schema creation mechanism
- Drop support for data_entity.generate_summary() and replace with improved data_entity.summarise()
- Drop support for upload models using baseline_files list of files
- Improved feature importance feature: new parameters in summarize():
  - importance_sample - a float value, used to sample the data while calculate the Feature importance
  - importance_target_label - an option to pass a label field name
- Remove deprecated task as a param to EntitiesValidator

## [4.2.3] 2021-12-07
- fix bug in binning for numeric features with null values

## [4.2.2] 2021-12-01
- Change the binning mechanism for numeric data entities

## [4.1.0] 2021-11-28
This release has breaking changes - add functionality for transaction:
- add functionality to upload data from s3 to superwise
- add functionality to upload data from gcs to superwise

## [4.0.0] 2021-11-23
This release has breaking changes - task changed following properties:
- task_description &rarr; description
- title &rarr; name
- task_type &rarr; removed

## [3.2.0] - 2021-11-16
This release has breaking changes.
Refactor tasks model

## [3.1.2] - 2021-11-15

Improve requirements.txt - lock versions and added jwt as a requirement.

remove DEBUG mode

log.debug added for each API call

## [3.1.0] - 2021-11-11
This release has breaking changes.
removed client_name as a param from superwise object


## [3.0.0] - 2021-10-19
This release has breaking changes.
We define new entity named transaction, which responsible to manage all the data send to superwise.

### Added
- Add Class Transaction, which have 2 methods to send data to superwise (file , batch).

### Removed
- Removed Data Class and send_file methods, for send data to superwise you should use the Transaction class.
