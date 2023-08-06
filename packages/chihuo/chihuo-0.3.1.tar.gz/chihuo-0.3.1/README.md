# chihuo: An Asynchronous Task Running Engine

chihuo is an asynchronous task running engine. It runs asynchronous tasks concurrently
from a queue which can be at memory, Redis, Lodis or Some MQ.

## The Loop

`ChihuoLoop` is the asynchronous engine core which responses to connect the backend queue
and distributes every tasks to the global event loop.

For a process, the chihuo create only one global event loop to run all asynchronous
tasks and the loop is running forever.

- `ChihuoLoop.start` method

  When a `ChihuoLoop` starts, it needs to add some primary tasks to the backend queue.
  The `start` function is the place to fire these priorities.

- `ChihuoLoop.add_task` method

  At anywhere and anytime, we can use the `add_task` method to add a task to backend queue.
  The task discription must be the tuple as `(task_id: str, task_info: jsonifiable object_)`
  e.g. `add_task(("task1", [1, 1+10]), ("task2", [2, 2+10]))`

- `ChihuoLoop.make_task` method

  Each classes which have implemented the `ChihuoLoop` class must to implement the `make_task`
  method for receiving the task's information that is added by `ChihuoLoop.add_task` to
  the backend queue.

- `ChihuoLoop.task_finish` method

  When a task is finished and is unneeded at future, we can tag the task as the `finished` state
  using the `task_finish` method. e.g. `task_finish(task_id)`. The task that is at `finished`
  state can't be add to backend queue again.

- `ChihuoLoop.task_unfinish` method

  When a task is at the `finished` state and we need to add it to queue again, we can use
  the `task_unfinish` method to set the task state to `unfinish`. Then, we can use
  `ChihuoLoop.add_task` to add the task to queue again.

- `ChihuoLoop.stop` property

  When the property `stop` to be set as True, the `ChihuoLoop` will stop pull the tasks from
  queue and exit.

## Demo

```python
# filename: abc.py

from chihuo import ChihuoLoop
from chihuo.common import SERVER_DEFAULT_CONFIG_PATH
import chihuo


class MyTasksA(ChihuoLoop):

    NAME = "my-tasksA"  # The unique id for backend queue server
    CONCURRENCY = 10   # The number of tasks running concurrently
    SERVER_CONFIG = SERVER_DEFAULT_CONFIG_PATH

    def __init__(self):
        super().__init__()

    async def start(self):
        for id in range(10):
            await self.add_task((str(i), {i ** 2}))

    async def make_task(self, task_id, task):
        print(f"my-task-A: {task_id}")
        print(f"power of {i} is {task}")

        # Talk chihuo that the task is finished
        await self.task_finish(i)


class MyTasksB(ChihuoLoop):

    NAME = "my-tasksB"  # The unique id for the loop
    CONCURRENCY = 10   # The number of tasks running concurrently
    SERVER_CONFIG = SERVER_DEFAULT_CONFIG_PATH

    def __init__(self):
        super().__init__()

    async def start(self):
        for id in range(10):
            await self.add_task((str(i), {i ** 2}))

    async def make_task(self, task_id, task):
        print(f"my-task-B: {task_id}")
        print(f"power of {i} is {task}")

        # Talk chihuo that the task is finished
        await self.task_finish(i)


if __name__ == '__main__':
    chihuo.run(MyTasksA, MyTasksB)
```

To Run the project, firstly we need to launch a backend queue server.
Here, we use a Lodis instance as default server.

Start a Lodis server:

```
LODIS_DB_PATH=/data/test-lodis LODIS_IP_PORT="127.0.0.1:8311" nohup /path/to/lodis &
```

Then, we write a configure file as `./server.json` (the `SERVER_DEFAULT_CONFIG_PATH`)
to connect the backend for our `MyTasksA` and `MyTasksB`.

```
backend=lodis
ip=127.0.0.1
port=8311
```

Now, we can run the script.

```
python3 abc.py
```

## Shutdown the Tasks

Defaultly, the global loop is running forever and we need to shutdown the loop by sending
a `INT (interrupt)` signal to the process. After the process received The `INT` signal, it will
set the property `stop` of instance which is implemented from `ChihuoLoop` to True and the
instance will stop all running tasks and send them back to queue, finally exit.
