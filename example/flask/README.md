# Bugsnag Flask demo

This Flask application demonstrates how to use Bugsnag with the Flask web framework for Python.

Install dependencies

```shell
pip install -r requirements.txt
```

Before testing it, open up the `server.py`
file and configure your API key.

```python
bugsnag.configure(
    "api_key": "YOUR_API_KEY_HERE"
)
```

Run the application.

```shell
python server.py
```

Next, open your project's dashboard on Bugsnag.

1. [crash](/example/flask/server.py#L18-L27)
<br/>
Crashes the library and sends a notification about the nature of the crash.
Basically, almost any unhandled exception sends a notification to Bugsnag.
Pressing this link would lead to an internal error, which is normal.

2. [crash and use callbacks](/example/flask/server.py#L29-L40)
<br/>
Before crashing, the library would append the Diagnostics tab with some
predefined information, attached by means of a callback.
Pressing this link would lead to an internal error, which is normal.

3. [notify](/example/flask/server.py#L42-L46)
<br/>
Bugsnag Python provides a way to send notifications on demand by means of
`bugsnag.notify()`. This API allows to send notifications manually, without
crashing your code.

4. [notify with meta data](/example/flask/server.py#L48-L65)
<br/>
Same as `notify`, but also attaches meta data. The meta data is any additional
information you want to attach to an exception. In this artificial case
additional information will be sent and displayed in new tabs such as Request
info and Resolve info.

5. [notify with context](/example/flask/server.py#L67-L74)
<br/>
The context shows up prominently in the list view so that you can get an idea of
where a problem occurred. You can set it by providing the `context` option.

6. [notify with severity](/example/flask/server.py#L76-L83)
<br/>
You can set the severity of an error in Bugsnag by including the severity option
when notifying Bugsnag of the error. Valid severities are `error`, `warning` and
`info`.