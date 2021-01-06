import serial
from serial.serialutil import SerialException
import click
from flask import Flask, request
from enum import Enum

app = Flask(__name__)

class CameraError(Exception):
    pass

class Action(Enum):
    OFF = 0
    ON = 1


class Command:
    OFF = b"off"
    ON = b"on"


class Camera:

    RDY = "rdy"

    _cam = None

    def __init__(self, device_port):
        self.device = serial.Serial(device_port, timeout=5)
        Camera._cam = self

    @classmethod
    def get(cls):
        if cls._cam is None:
            raise Exception("Not started")
        return cls._cam

    @classmethod
    def init(cls, device_port):
        if Camera._cam is not None:
            raise Exception("Init called twice")
        return cls(device_port)
    
    def reset(self):
        self.device.close()
        try:
            self.device.open()
        except SerialException:
            pass
        return self

    def performAction(self, action):
        try:
            if action is Action.ON:
                self.device.writelines([Command.ON])
            if action is Action.OFF:
                self.device.writelines([Command.OFF])
        except SerialException:
            return False
        return True

    def __repr__(self):
        return f"<Camera device={self.device.port} open={self.device.is_open}>"


@app.route("/set", methods=["POST"])
def toggle():
    try:
        action = Action[request.get_data().decode()]
    except KeyError:
        return "fail", 400

    if Camera.get().performAction(action):
        return "ok"
    else:
        try:
            if Camera.get().reset().performAction(action):
                return "ok"
            else:
                return "not connected", 500
        except CameraError:
            return "whoops", 500


@click.command()
@click.option("--device-port", type=str)
def run(device_port):
    """
    Run the server
    """
    try:
        Camera.init(device_port)
    except SerialException:
        raise click.UsageError("Device not found or invalid, please start with device connected")
    app.run(debug=True)


if __name__ == "__main__":
    run()