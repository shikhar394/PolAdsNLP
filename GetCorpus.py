import configparser
import datetime
import html
import json
import os
import re
import sys
import time
from collections import namedtuple

import psycopg2
import psycopg2.extras
import requests
from unidecode import unidecode

if len(sys.argv) < 2:
    exit("Usage:python3 import_ads_to_db.py import_ads_to_db.cfg")

config = configparser.ConfigParser()
config.read(sys.argv[1])

TEXTFILE = config['LOCATION']['TEXTFILE']
HOST = config['POSTGRES']['HOST']
AD_DBNAME = config['POSTGRES']['DBNAME_ADS']
LABEL_DBNAME = config['POSTGRES']['DBNAME_LABELS']
USER = config['POSTGRES']['USER']
PASSWORD = config['POSTGRES']['PASSWORD']
DBAuthorize = "host=%s dbname=%s user=%s password=%s" % (HOST, AD_DBNAME, USER, PASSWORD)

ads_connection = psycopg2.connect(DBAuthorize)
ads_cursor = ads_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

DBAuthorize = "host=%s dbname=%s user=%s password=%s" % (HOST, LABEL_DBNAME, USER, PASSWORD)
labels_connection = psycopg2.connect(DBAuthorize)
labels_cursor = labels_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

TagRemove = re.compile(r'<[^>]+>')


def RemoveTags(text):
    return TagRemove.sub("", text)

def CleanText(text):
    return unidecode(RemoveTags(html.unescape(text.strip())))

if __name__ == "__main__":
  IDs = set()
  TextCorpus = {} #ID:Ad Text
  IDQuery = """
    select distinct(ad_id) from labels
    """
  labels_cursor.execute(IDQuery)
  for ID in labels_cursor.fetchall():
    IDs.add(ID[0])

  TextQuery = """
    select archive_id, text from ads where archive_id in (%s)
    """ 
  ads_cursor.execute(TextQuery, IDs)

  for result in ads_cursor.fetchall():
    TextCorpus[result['archive_id']] = CleanText(result['text'])
