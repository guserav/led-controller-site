import flask
import functools
import paho.mqtt.client as mqtt
from os.path import expanduser


app = flask.Flask(__name__)

CONF_FILE = expanduser('~/.config/led_controller_web/config.ini')
BROKER = "jackson"
TOPIC = "/topic/esp32_led"

class NavItem():
    def __init__(self, internal, name):
        self.internal = internal
        self.name = name


def getGeneralArgs(current):
    return {
        'navitems': [
        ],
        'current_nav': current,
    }


def wrapCon(func):
    @functools.wraps(func)
    def inner(*args, client=None, **kwargs):
        if client is None:
            client = mqtt.Client("Temperature_Inside")
            client.connect(BROKER)
            ret = func(*args, client=client, **kwargs)
            client.disconnect()
            return ret
        else:
            return func(*args, client=client, **kwargs)
    return inner


def wrapCalls(name):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            func(*args, **kwargs)
            return flask.render_template('home.html',
                    last_action=name,
                    **getGeneralArgs('index'))
        return inner
    return decorator


@app.route('/')
@wrapCalls(None)
def index():
    pass


@app.route('/turnoff')
@wrapCon
@wrapCalls('turnoff')
def turnoff(client=None):
    client.publish(TOPIC, 'turnoff')


@app.route('/recover')
@wrapCon
@wrapCalls('recover')
def recover(client=None):
    client.publish(TOPIC, 'recover')
