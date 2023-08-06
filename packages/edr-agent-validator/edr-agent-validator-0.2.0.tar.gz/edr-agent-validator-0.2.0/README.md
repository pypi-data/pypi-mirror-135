This is an EDR agent validator project for the Red Canary Engineering Interview.

I created this project using [Typer](https://typer.tiangolo.com/) and you can manage all it's dependencies with [Poetry](https://python-poetry.org/).

It's using [`psutil`](https://github.com/giampaolo/psutil) for cross platform process information gathering and uses [`desert`](https://desert.readthedocs.io/en/stable/) to serialize its dataclasses to logs (for activity tracking for correlation with EDR agents).

The arguments and defaults are all documented in the help menu. You can install it with pip via `pip install edr-agent-validator`.

Try it out! By default all actions are appended as JSON to a file in the directory you run the tool in called `activity_log.txt`, but this can be configured.

It's a fairly simple tool, it uses the sockets api for it's network connections, basic python file I/O apis for file creation, modifying, and deletion, and the [`subprocess.Popen`](https://docs.python.org/3/library/subprocess.html#subprocess.Popen) api for launching a background process.

For the network activity component, it can send bytes over UDP or TCP.

Most of the time I spent learning how to build an eloquent CLI with Typer and the new (to me) python type annotions. It was quite a fun learning exercise!

One thing to keep in mind about the activity logging is that during the printing/serialization of a dict, the key order is not consistent. This makes the logs more suited for parsing by machines than humans, as each line is it's own json object with it's keys in an arbitrary order. I'd probably improve this in the future to have a consistent serialization order.
