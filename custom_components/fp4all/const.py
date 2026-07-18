"""
FP4All Local for Home Assistant

Version : 0.3
Build   : 2.0
File    : const.py

const platform for FP4All.
"""
from __future__ import annotations

from datetime import timedelta

DOMAIN = "fp4all"

NAME = "FP4All Local"

VERSION = "0.2.0"

MANUFACTURER = "FP4All"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

STATUS_XML = "status.xml"
STATUS_HTML = "status.htm"
HISTORY_HTML = "daysview.htm"
INDEX_HTML = "index.htm"
ERRORLOG_HTML = "errorlog.htm"

SERVICE_DOWNLOAD_HISTORY = "download_history"

HISTORY_FOLDER = "fp4all_history"