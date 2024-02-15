import urllib.parse

import flask

from flask import Flask, request
from .pay_helper import get_payment


app = Flask(__name__)


@app.route("/payment", methods=["POST"])
async def payment_notification_handler():
    """hundle payments events"""
    if request.headers.get("content-type") == "application/x-www-form-urlencoded":
        name = request.stream.read().decode("utf-8")
        parse_data = urllib.parse.parse_qs(name)
        tg_id = int(parse_data.get("label", [""][0]))
        await get_payment(tg_id=tg_id)
        return "Successful", 200
    else:
        flask.abort(403)
