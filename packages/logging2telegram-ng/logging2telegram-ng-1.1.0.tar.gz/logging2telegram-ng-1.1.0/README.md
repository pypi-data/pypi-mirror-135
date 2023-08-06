# logging2telegram-ng

This is a fork of [logging2telegram](https://github.com/tezmen/logging2telegram),
aiming to integrate some features from [telegram-logging](https://pypi.org/project/telegram-logging/).

Fastest and simple handler for stream logging output to telegram chats. 

[![N|Solid](https://img.shields.io/pypi/pyversions/logging2telegram-ng.svg)](https://pypi.python.org/pypi/logging2telegram-ng)

### Installation
You can install or upgrade package with PIP:
```
$ pip install logging2telegram-ng --upgrade
```
Or you can install from source with:
```
$ git clone https://github.com/jmfernandez/logging2telegram-ng.git
$ cd logging2telegram-ng
$ python setup.py install
```
...or install from source buth with pip
```
$ pip install git+https://github.com/jmfernandez/logging2telegram-ng.git
```

### Example
```python
import logging.config
import logging

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'tg_full_ng': {
            '()': 'log2tg_ng.NgHtmlFormatter',
        }
    },
    'handlers': {
        'telegram': {
            'level':     'DEBUG',
            'class':     'log2tg_ng.NgTelegramHandler',
            'formatter': 'tg_full_ng',
            'disable_web_page_preview': True,
            'token':     'BOT:TOKEN',
            'ids':       [123,132,321],
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['telegram']
        }
    },
})

def show():
	logger = logging.getLogger('myapp')
	logger.warning('we have <b>a</b> warning')

if __name__ == '__main__':
	show()

```
For custom formating:

```python
'formatters': {
    'tg_full': {
        '()': 'log2tg_ng.NgHtmlFormatter',
        'use_emoji': False,
        'format': '<b>%(level)s</b> %(filename)s: %(message)s <code>%(exc_text)s</code>'
    }
}
```
