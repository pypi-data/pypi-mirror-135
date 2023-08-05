#!/usr/bin/env python3
# Filename: core.py

"""
Database utilities.

"""
import requests
import json
import os

from km3db.logger import log

USER_INPUT = input
BASE_URL = "https://dia.km3net.de"
COOKIE_FILENAME = os.path.expanduser("~/.km3netdia_cookie")


class DBManager:
    """
    Low level class to access the DIA DB.

    The login information are provided by the user, and stored in a
    cookie for later usage. The user can extract this login info from
    the 8 last digits of the QR code that was provided to access the
    DIA website.

    Parameters:
    -----------
    url: str
       DIA server address. Default: "https://dia.km3net.de"
    container: str
       Return type from the wrapper. Can be `nt` for tupples, `pd` for pandas. Default: `nt`
    """

    def __init__(self, url=None, container="nt"):
        self._db_url = BASE_URL if url is None else ulr
        self._container = container
        self._session_cookie = None

    def get(self, url, OID=None):
        "Get HTML content"
        target_url = self._db_url + "/" + url
        print(target_url)
        x = None
        data = {"km3uname": OID}
        if data["km3uname"] is None:
            data["km3uname"] = self._request_session_cookie()

        try:
            x = requests.post(target_url, data, verify=False)

        except Exception as E:
            print(E)

        if x.text == "":
            log.warning(f'Empty answer from "{target_url}"')
            return None

        if self._container == "nt":
            return json.loads(x.text)

        elif self._container == "pd":
            import pandas

            return pandas.DataFrame(json.loads(x.text))

    @property
    def session_cookie(self):
        """Wrap the OID retrieving process"""
        if self._session_cookie is None:
            self._session_cookie = self._request_session_cookie()
        return self._session_cookie

    def _request_session_cookie(self):
        """Create OID cookie for permanent session."""
        if os.path.exists(COOKIE_FILENAME):
            log.info("Using cookie from %s", COOKIE_FILENAME)
            with open(COOKIE_FILENAME) as fobj:
                OID = fobj.read()
                return OID

        # The OID can also be set via the environment
        cookie = os.getenv("KM3NET_DIA_OID")
        if cookie is not None:
            log.info("Using OID from env ($KM3NET_DIA_OID)")
            return cookie

        # Last resort: we ask interactively
        OID = USER_INPUT("Please enter your KM3NeT DIA username: ")
        while self.check_OID_validity(OID) == False:
            OID = USER_INPUT("Please enter your KM3NeT DIA username: ")

        OID = "xxx." + OID
        log.info("Writing session cookie to %s", COOKIE_FILENAME)
        with open(COOKIE_FILENAME, "w") as fobj:
            fobj.write(f"xxx.{OID}")

        return OID

    def check_OID_validity(self, OID):
        """Check OID the validity to log to DIA"""
        result = self.get(
            f'/doquery.php?REQ=SELECT * FROM Operators WHERE KM3db_OID="{OID}";',
            OID="xxx." + OID,
        )
        if result is None:
            log.error("Hum, the OID appears to be wrong ...")
            return False
        return True

    def get_SQL(self, query):
        "Do SQL query to DIA DB"
        query_url = "/doquery.php?REQ=" + query
        if query_url[-1] != ";":
            query_url += ";"

        return self.get(query_url)
