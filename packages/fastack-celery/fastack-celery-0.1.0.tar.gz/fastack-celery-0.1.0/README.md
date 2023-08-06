# fastack-celery

Simple package to integrate celery with fastack.

## To-do

There are several to-do lists for the future

- [ ] See [#1](https://github.com/fastack-dev/fastack-celery/issues/1)

## Installation

```
pip install fastack-celery
```

## Usage

### Create celery app

Copy the code below and put it in `app/main.py`:

```py
from fastack_celery import make_celery
celery = make_celery(app)
```

You can also pass parameters to the celery app.

### Configuration

For celery configuration, you can create it via `Celery` class in your app settings. For example:

```py
# app/settings/local.py
class Celery:
    broker_url = "amqp://strong_user:strong_password@localhost:5672/celery_vhost"
    result_backend = "redis://localhost:6900/0"
```

For other celery configurations, see here https://docs.celeryproject.org/en/stable/userguide/configuration.html#new-lowercase-settings

### Create a task

You can create tasks using the `shared_task` decorator:

```py
# app/tasks.py

# Sample task from examples/celery/app/tasks.py
@shared_task
def counter_task(id: int):
    session = db.open()
    with session.begin():
        obj: Counter = session.query(Counter).where(Counter.id == id).first()
        if obj:
            print(f"start counting #{id}")
            obj.counter += 1
            state = obj.state
            if state is None or state == Counter.State.NOT_IN_QUEUE:
                obj.state = Counter.State.NOT_IN_QUEUE
            elif state == Counter.State.TERMINATED:
                task_id = obj.task_id  # or current_task.request.id
                celery.control.revoke(task_id, terminate=True)
                obj.task_id = None
            else:
                obj.state = Counter.State.IN_QUEUE
                counter_task.apply_async(args=(id,), countdown=1, task_id=obj.task_id)

            obj.save(session)

        else:
            print(f"Object with id #{id} not found")
```

By default, all tasks must be stored in `app/tasks.py` which will be automatically imported by the `make_celery` function.

### Running celery workers

```
cd your-project
celery -A app.main:celery worker -l info
```
