from datetime import timedelta

DOMAIN = "fp4all"

NAME = "FP4All Local"

VERSION = "3.1.9"

MANUFACTURER = "FP4All"

#
# Update interval
#

CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

UPDATE_INTERVALS = {
    "Realtime": 1,
    "10 seconds": 10,
    "30 seconds": 30,
    "1 minute": 60,
    "5 minutes": 300,
}

#
# Bestanden
#

STATUS_XML = "status.xml"
STATUS_HTML = "status.htm"
HISTORY_HTML = "daysview.htm"
INDEX_HTML = "index.htm"
ERRORLOG_HTML = "errorlog.htm"

SERVICE_DOWNLOAD_HISTORY = "download_history"

HISTORY_FOLDER = "fp4all_history"