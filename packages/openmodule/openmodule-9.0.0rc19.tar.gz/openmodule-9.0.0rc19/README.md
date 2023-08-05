# OpenModule V2

Some additional documentation:

* [Openmodule Core](docs/core.md)
* [RPC Server / Client](docs/rpc.md)

## Changes

Breaking changes are annotated [here](docs/migrations.md).

To quickly check if your service is susceptible to a known issue have a look [here](docs/migrations.md).

## Coding Standard

For ARIVO developers we have defined a simple coding standard [here](docs/coding_standard.md)

## Features

The openmodule package provides a lot of features:

### Settings

The openmodule package uses a global lazy configuration `openmodule.config.settings`. This setting includes some
standard parameters defined in `openmodule.config.GlobalSettings` and parameters from a customizable module. To specify
the module you can call `settings.configure(module)` or you can set the environment variable `SETTINGS_MODULE`. Per
default settings looks for the `config` module (it also looks for the `tests/config` module first for test cases)

#### Models

Inherit from `OpenModuleModel` or in case of ZMQ messages from `ZMQMessage`. Models use
pydantic ([docs](https://pydantic-docs.helpmanual.io/usage/types/)), check openmodule.models.* for some examples (e.g.
PresenceBaseMessage for alias)

### Core

The base of the new openmodule, every package should have exactly one. The core handles various things:

* sentry
* logging
* dsvgo
* messaging
* health
* alerting
* database

``` python
core = init_openmodule(config, **kwargs)
shutdown_openmodule()
```

#### Messaging

##### Receiving messages

The core handles message distribution with a dispatcher. You only need to register your callback.

* **register_schema**: Automatically create a schema for your message handler and its models -> Beware that you need to
  document your handler method

```python
core.messages.register_handler(b"topic", MessageClass, callback, filter={type = "demo"}, register_schema = True)
```

It may also be used together with an event listener to provide further functionality

```python
event_listener = EventListener(log=logger)
core.messages.register_handler(b"topic", MessageClass, event_listener, filter={type = "demo"})
...
event_listener.append(some_function)
```

#### Sending messages

It is even easier to send messages

```python
message = ZMQMessage(name=core.config.NAME, type="demo")
core.publish(message, b"topic")
```

#### Health

Due to the new convention, the health message should only represent if the service is still alive. This is done
automatically by the core. If you need to specify some meta data or errors you can pass your handler to the core or set
it later

```python
def healthy() -> HealthResult:
    if error:
        return health_error("we have an error", meta=dict(error="error"))
    return health_ok(meta=dict(this="is_easy"))


core = init_openmodule(config, health_handler=healthy)
# or
core.health.health_hanlder = healthy
```

#### Alerting

The new core also includes an alert handler.

```python
core.alerts.send(...)
alert_id = core.alerts.get_or_add_alert_id(...)
core.alerts.send_with_alert_id(alert_id, ...)
```

#### Database

The openmodule package now also feature a simple database which can be also specified during the template creation. If
you missed it there, just copy the directory src/database from the template. For more infos see [here](docs/database.md)

### RPCs

A new RPC server/client was implemented. It works like before and also includes better filtering:

* if a channel is provided for a filter, only rpcs of that channel will be subject to that filter
* if a type is provided for a filter, only rpcs of that type will be subject to that filter
* **register_schema**: Automatically create a schema for your rpc and its models -> Beware that you need to document
  your handler method

```python
def handler(request: AccessRequest):
    """
    awesome description
    """


rpc = RPCServer(config=core.config, context=core.context)
rpc_server.add_filter(self._backend_filter, "backend", "auth")
rpc_server.register_handler("backend", "auth", request_class=AccessRequest,
                            response_class=AccessResponse, handler=handler, register_schema=True)
rpc.run()
```

### Utils

#### Api

We implemented a very basic Api class you can use for http request and that handles errors and authentication. Either
inherit it or create a class.

```python
api = Api(**kwargs)
try:
    res = api.post("some_url", payload=stuff)
except ApiException as e:
    if e.retry:  # <- makes sense to try again - timeouts or server not available ...
        ...
```

#### Backend

There is also a basic implementation of a backend that provides registration and message passing.

```python
class MyBackend(Backend):
    def check_access(self, request: AccessRequest) -> List[Access]:
        ...

    def check_in(self, message: CountMessage):
        ...

    def check_out(self, message: CountMessage):
        ...
```

#### Charset

Useful functions for character manipulation

#### Connection Status

Helper class that checks the connection status of ogclient to our server:

```python
connection_status = ConnectionStatusListener(core.messages)
connection_status.on_connect.append(some_function)
connection_status.on_disconnect.append(some_function)
```

#### Matching

Useful functions for license plate matching

#### Presence

Helper class for listening to presence messages.

```python
presence_listener = PresenceListener(core.messages)
presence_listener.on_enter.append(some_function)
```

## Documentation

Openmodule >= 3.0.5 features automatic generation of Rpc and Message Schemas including their models. The generation uses
data that is generated during the test runs to create an OpenApi Schema. Your RPCs and Message handlers are
automatically documented if:

* You use the message dispatcher of the core (OpenModuleCoreTestMixin)
* You use the RPCServer of Openmodule

You can also register models yourself if you want them documented, but you may need to save the Schema in this case:

```python
from openmodule.utils.schema import Schema

Schema.save_model(Model)
Schema.save_rpc(channel, type, request, reqponse, handler)
Schema.save_message(topic, message_class, handler, filter)

Schema.to_file()
```

With default parameters, you need to document your handler functions with a doc string, that is then included as a
description.

## Testing

A separate package for testing openmodule packages exists within openmodule - openmodule-test. For more infos
see [here](docs/testing.md)
