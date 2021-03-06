from flask import Flask, redirect, url_for, request, render_template, current_app
from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_api import status
import logging
import sys
import datetime as dt
import sqlite3
import inspect

from api.db import get_db

bp = Blueprint("applications", __name__)


@bp.route("/api/applications", methods=["GET"])
def getApplications():
    data = []

    # Database select
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT id,app.name,app.environment,app.version,app.country,app.provider,app.project,app.region,app.datacenter,app.services FROM application as app").fetchall()
    db.close()
    for row in rows:
        data.append({
          "id": row[0],
          "name": row[1],
          "environment": row[2],
          "version": row[3],
          "country": row[4],
          "provider": row[5],
          "project": row[6],
          "region": row[7],
          "datacenter": row[8],
          "services": row[9],
        })

    return jsonify(data)

@bp.route("/api/applications", methods=["POST"])
def addApplication():
    app_name = request.form.get("app_name")
    app_env = request.form.get("app_env")

    appName = "{}".format(app_name)
    appEnv = "{}".format(app_env)

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT app.name,app.environment FROM application app WHERE name = ? AND environment = ?", [appName, appEnv]).fetchall()
    if len(rows) > 0:
        db.close()
        current_app.logger.info("Application {} with environment {} already exists.".format(appName, appEnv))
        return { "msg": "Application '{}' with environment '{}' already exists.".format(appName, appEnv) }, status.HTTP_409_CONFLICT

    cur = db.cursor()
    cur.execute('INSERT INTO application(name, environment) VALUES (?, ?)', (appName, appEnv))
    db.commit()

    db.close()

    return { "msg": "Application '{}' with environment '{}' added to landscape.".format(appName, appEnv) }, status.HTTP_201_CREATED

@bp.route("/api/applications/<int:app_id>", methods=["PUT"])
def updateApplication(app_id):
    appId = "{}".format(app_id)
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
      appServices = "{}".format(request.form.get("app_services"))

    db = get_db()
    cur = db.cursor()
    try:
      cur.execute('UPDATE application SET version=?, country=?, provider=?, project=?, region=?, datacenter=?, services=? WHERE id=?', (appVersion, appCountry, appProvider, appProject, appRegion, appDatacenter, appServices, app_id))
      db.commit()
      cur.close()
      db.close()
      return { "msg": "Application '{}' have been updated.".format(appId) }, status.HTTP_200_OK
    except sqlite3.Error as e:
      cur.close()
      db.close()
      logging.error("{}, {}, {}".format(inspect.currentframe().f_code.co_name, status.HTTP_400_BAD_REQUEST, e))
      return { "msg": "An error occured when updating application '{}'.".format(appId) }, status.HTTP_400_BAD_REQUEST



@bp.route("/api/applications/<int:app_id>", methods=["DELETE"])
def deleteApplication(app_id):
    appId = "{}".format(app_id)

    db = get_db()
    cur = db.cursor()
    try:
      cur.execute('DELETE FROM application WHERE id = ?', [appId])
      db.commit()
      db.close()
      return { "msg": "Application '{}' have been deleted.".format(appId) }, status.HTTP_200_OK
    except sqlite3.Error as e:
      db.commit()
      db.close()
      logging.error("{}, {}, {}".format(inspect.currentframe().f_code.co_name, status.HTTP_400_BAD_REQUEST, e))
      return { "msg": "An error occured when deleting application '{}'.".format(appId) }, status.HTTP_400_BAD_REQUEST

