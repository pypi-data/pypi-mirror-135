# Django pubsub

Django Pubsub wrapper.


## Installation with requirements.txt
```
djangopubsub
```

### With PIP

```bash
$ pip install djangopubsub
```

## Add app to django settings
```
INSTALLED_APPS = (
    ...,
    'djangopubsub'
)
```

## Available settings and defaults:
```python
BASE_DIR = ''  # Root directory for handlers lookup
EVENT_HANDLERS_DIR_NAME = 'event_handlers'  #  Directory with handlers on every app module
HANDLER_FILES_PREFIX = 'handlers_' # handlers file prefix
REDIS_HOST = 'localhost'
REDIS_PORT = 6379 
PUB_SUB_EMIT = True  # Avoid to emit message when emit is called (for tests)
```

## Decorator
```python
@on_event('EVENT_NAME')
def func_to_execute(data):
    pass
```

## Pubsub emit
```python
from djangopubsub.djangoPubSub import DjangoPubSub
DjangoPubSub().emit('EVENT_NAME', {})
```

## Pubsub receiver
Needs redis running on port:REDIS_PORT
```commandline
python manage.py runpubsubreceiver --settings=your_proyect.settings
```
