from flask import Flask, redirect, url_for, request, render_template, current_app
from flask import Blueprint
from flask_cors import CORS
from flask_api import status
import logging
import sys
import sqlite3
import json

from api.db import get_db

bp = Blueprint("health", __name__)


@bp.route("/api/health", methods=["GET"])
def getHealth():
    data = []

    logging.info(current_app)

    return json.dumps(data)

