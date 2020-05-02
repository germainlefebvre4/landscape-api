from flask import Flask, redirect, url_for, request, render_template, current_app
from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_api import status
import logging
import sys
import datetime as dt
from tinydb import Query
import inspect
import json

from api.db import get_db

bp = Blueprint("applications", __name__)


@bp.route("/api/applications", methods=["GET"])
def getApplications():
    data = []

    # Database select
    db = get_db()
    table = db.table('application')
    data = table.all()

    return jsonify(data)

@bp.route("/api/applications", methods=["POST"])
def addApplication():
    app_name = request.form.get("app_name")
    app_env = request.form.get("app_env")

    appName = "{}".format(app_name)
    appEnv = "{}".format(app_env)

    db = get_db()
    App = Query()
    table = db.table('application')
    rows = table.search(
      (App.name == appName) &
      (App.environment == appEnv)
    )
    if len(rows) > 0:
        current_app.logger.info("Application {} with environment {} already exists.".format(appName, appEnv))
        return { "msg": "Application '{}' with environment '{}' already exists.".format(appName, appEnv) }, status.HTTP_409_CONFLICT

    table.insert(
      {
        "name": appName,
        "environment": appEnv,
        'version': None,
        'country': None,
        'provider': None,
        'project': None,
        'region': None,
        'datacenter': None,
        'services': None,
      }
    )

    return { "msg": "Application '{}' with environment '{}' added to landscape.".format(appName, appEnv) }, status.HTTP_201_CREATED

@bp.route("/api/applications/<int:app_id>", methods=["PUT"])
def updateApplication(app_id):
    appId = app_id
    appVersion = None
    appCountry = None
    appProvider = None
    appProject = None
    appRegion = None
    appDatacenter = None
    appServices = None
    if request.form.get("app_version"):
      appVersion = "{}".format(request.form.get("app_version"))
    if request.form.get("app_country"):
      appCountry = "{}".format(request.form.get("app_country"))
    if request.form.get("app_provider"):
      appProvider = "{}".format(request.form.get("app_provider"))
    if request.form.get("app_project"):
      appProject = "{}".format(request.form.get("app_project"))
    if request.form.get("app_region"):
      appRegion = "{}".format(request.form.get("app_region"))
    if request.form.get("app_datacenter"):
      appDatacenter = "{}".format(request.form.get("app_datacenter"))
    if request.form.get("app_services"):
      # appServices = "{}".format(request.form.get("app_services"))
      appServices = request.form.get("app_services")

    db = get_db()
    table = db.table('application')
    try:
      table.update(
        {
          'version': appVersion,
          'country': appCountry,
          'provider': appProvider,
          'project': appProject,
          'region': appRegion,
          'datacenter': appDatacenter,
          'services': json.loads(appServices),
        },
        doc_ids = [app_id]
      )
      return { "msg": "Application #{} have been updated.".format(appId) }, status.HTTP_200_OK
    except:
      logging.error("{}, {}, {}".format(inspect.currentframe().f_code.co_name, status.HTTP_400_BAD_REQUEST, {}))
      return { "msg": "An error occured when updating application #{}. Please provide a JSON with double quoted key and value.".format(appId) }, status.HTTP_400_BAD_REQUEST



@bp.route("/api/applications/<int:app_id>", methods=["DELETE"])
def deleteApplication(app_id):
    appId = app_id

    db = get_db()
    table = db.table('application')
    App = Query()
    doc = table.get(
      doc_id = appId
    )
    if doc:
      try:
        table.remove(doc_ids=[appId])
        return { "msg": "Application '{}' have been deleted.".format(appId) }, status.HTTP_200_OK
      except:
        logging.error("{}, {}, {}".format(inspect.currentframe().f_code.co_name, status.HTTP_400_BAD_REQUEST, {}))
        return { "msg": "An error occured when deleting application {}".format(appId)}
    else:
      return { "msg": "Application #{} does not exist.".format(appId) }, status.HTTP_400_BAD_REQUEST

