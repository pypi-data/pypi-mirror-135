#!/usr/bin/env python3
# Filename: DOM_integration_summary.py

"""
Module to get summary of DOM integration in a convenient format
"""

import km3dia
import pandas as pd
import numpy as np

from km3db.logger import log


def remove_dup_columns(frame):
    """Remove duplicated columns from a pandas DataFrame"""
    keep_names = set()
    keep_icols = list()
    for icol, name in enumerate(frame.columns):
        if name not in keep_names:
            keep_names.add(name)
        keep_icols.append(icol)
    return frame.iloc[:, keep_icols]


def measurement_name(tid, mid):
    """Format T_id and M_id into a string"""
    return "{:02d}_{:03d}".format(int(tid), int(mid))


class DOMIntegrationSummary:
    """
    Product a formated summary of the DOM integration
    information available in the DIA DB
    """

    def __init__(self, DIAManager=None):
        self.DIAManager = DIAManager
        if self.DIAManager is None:
            self.DIAManager = km3dia.DBManager(container="pd")

        self._test_results = None

    @property
    def test_results(self):
        """Wrapper for accessing test results"""
        if self._test_results is None:
            self._test_results = self._get_test_results()
        return self._test_results

    def _get_test_results(self):
        """Generate the test results DataFrame"""
        # Get all the measurements stored in the DIA DB
        req = "SELECT * FROM Test ts"
        req += " INNER JOIN Measure ms ON ts.E_T_id=ms.E_T_id"
        req += " INNER JOIN ASSIGNED_DOM ad on ad.UPI=ts.UPI"
        req += " INNER JOIN Bench bc on bc.B_id=ad.B_id"

        df = self.DIAManager.get_SQL(req)
        log.info(f"{df.shape[0]} measurement loaded.")

        # Link the measurement T_ID, M_ID and M_T_ID to measurement label
        measurement_map = {}
        df_tm = self.DIAManager.get_SQL("SELECT * FROM Test_Measures").astype(
            {"T_id": int, "M_id": int, "M_T_id": int}
        )
        df_tm["Measurement"] = np.vectorize(measurement_name)(
            df_tm["T_id"], df_tm["M_id"]
        )

        for ind, row in df_tm.iterrows():
            if row["T_id"] == 3:
                df_tm.at[ind, "Name"] += " (func)"
            if row["T_id"] == 4:
                df_tm.at[ind, "Name"] += " (accept)"

        measure_name_dict = df_tm.set_index("Measurement")["Name"].to_dict()

        # Map the REPAIR states to initial steps
        T_id_mapReplace = {7: 2, 8: 3, 9: 4, 10: 5, 11: 6}

        # Pass from Narrow to wide format for measurement
        df = remove_dup_columns(df)
        df = df.dropna(subset=["VALUE"])
        df.replace({"T_id": T_id_mapReplace}, inplace=True)

        # Get rid of larger T_id, corresponding to BM integration
        df = df[df["T_id"].astype(int) <= 6]

        df.sort_values("M_Time", inplace=True)
        df["Measurement"] = np.vectorize(measurement_name)(df["T_id"], df["M_id"])

        self.measurements = df

        # Define the list of information we want to keep but not measurement-related
        DOM_info = [
            "PBS",
            "VARIANT",
            "VERSION",
            "SERIAL",
            "SiteID",
            "PhaseID",
            "Complete",
            "Registered",
            "NotConform",
            "Repair",
            "B_Details",
            "B_type",
        ]

        df_DOM = df.drop_duplicates(subset=["UPI"], keep="last").set_index("UPI")
        df_DOM = df_DOM[DOM_info]

        # Sorted in time, so keep the last result for each measurement
        df = df.drop_duplicates(subset=["UPI", "Measurement"], keep="last")

        # Use pivot to produce a wide version of the measurement table
        df = df.pivot(index="UPI", columns="Measurement", values="VALUE")

        # Sort by label, to sort by step
        df.columns = np.sort(df.columns)
        df.rename(columns=measure_name_dict, inplace=True)

        # Merge generic info and measurement info
        df = pd.concat((df_DOM.loc[df.index], df), axis=1)
        df = df[df["SERIAL"].astype(int) > 2]
        df = df.reset_index().set_index(["SERIAL", "UPI"])

        return df
