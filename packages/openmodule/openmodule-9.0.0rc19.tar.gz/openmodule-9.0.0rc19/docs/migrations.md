# Breaking Version Changes

## 9.0.0

This version refactored the RPC client, especially asynchronous retrieval of rpc results. See
the [RPC Documentation](./rpc.md) for more information about asynchronous rpc calls and the RPC Client. Critically the
common issue of "cannot do RPC's while inside an RPC handler" has been solved by creating a dedicated thread for the rpc
client and some future openmodule core internals which should not be blocked by badly behaving user code anyways.

* the `RPCClient.check_results()` function was removed, and is replaced by a `.result()`.
* The RPCClient together with the HealthHandler how has a dedicated thread in the open module core. It is discouraged to
  create an rpc client of your own. Please use the rpc client of openmodule core. A deprecation warning hints this also.

Also some things have been deprecated and will be removed

* the RPC Server no longer requires a config object to be passed. It takes the global openmodule settings instead.
* the RPC Client now warns if a `OpenModuleCore` is passed to it's constructor
* the RPC Client now warns if a dictionary is used for RPC requests
* MockEvent's `reset_call_count()` and `reset_all_call_counts()` was replaced by analog `reset_mock()`
  and `reset_all_mocks()`

Furthermore, fields were renamed in python (with aliases, so the serialized version stays the same):

* `Backend -> AccessRequest: id -> medium_id`
* `Backend -> MediumAccesses: id -> medium_id, type -> medium_type`
* `Backend -> CountMessage: id -> medium_id`
* `Backend -> CountMessage: previous_id ->  previous_medium_id`

In the backend test utils the `create_access_request()` method was removed.

The default value for `match_type` in `MessageDispatcher.register_handler` is now `True`.

## 8.1.1

This version includes breaking changes for testcases only.

* The main test mixin was refactored and `exception_in_function` was removed.

## 8.0.0

* Drops support for python 3.7

## 7.0.0

* Removed all support for direct config changes in all test classes. Now everything is controlled by the lazy settings.

## 6.1.6

* Removed redis_kv from Version 6.1.5

## 6.1.2

* Please add the following snippet to your `tox.ini`, before `[testenv:clean]`.
  ```
  [testenv:openmodule_test]
  deps =
  skip_install = true
  changedir = {toxinidir}/src
  whitelist_externals = bash
  commands = bash -c 'if grep -ri "openmodule_test" . ; then echo ; echo "You must not import openmodule_test inside the openmodule project!" ; echo ; exit 1; else exit 0 ; fi'
  ```
* SETTINGS_MODULE now needs a module instead of a path

## 6.1.0

* The new lazy settings need a `src/config.py` file or you need to set the `SETTINGS_MODULE` environment variable to a
  module

## 6.0.0

* All `OpenModuleModel` fields of type `datetime` require a timezone validator which is checked during testing /
  debugging. After this version **all datetime objects should be timezone naive**.
* All sqlalchemy database models disallow the use of `DateTime` and require the use of `TZDateTime`. This preemptively
  avoids bugs, because sqlalchemy with sqlite looses timezone information.
* `models.backend.Access` now uses timezone naive datetimes instead of timezone aware datetimes. The `is_valid` method
  still accepts both.
* in MessageDispatcher `raise_validation_errors` and `raise_handler_errors` are now required to be named arguments
* `MockEvent.wait_for_call()` now raises a Timeout error instead of an assertion error

## 5.0.0

* AlertHandler.send() and get_or_add_alert_id() were refactored:
    * `source` is now a keyword argument, with default value `""`
    * most arguments are forced to keyword arguments

## 4.0.0

* the Category Enum was renamed to AccessCategory
* all member variables of Category/AccessCategory are lowercased
* the Medium Enum was renamed to MediumType
* all member variables of Medium/MediumType are lowercased
* the default database folder changed to a mounted volume

## 3.0.0

* the registration of bases for the database changed from `register_bases([...])` to `run_env_py([...])`

## 2.0.0

* Pydantic models are now defined in a model folder
