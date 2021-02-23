#!/usr/bin/env python3

import csv
import os
import numpy as np
from operator import itemgetter
from scipy.stats import linregress


def create_peak_list(raw_import_data):
    """Convert mzmine scan by scan peak data into basic list of lists with headers:
    sample, peak id, mz, rt, rt data, intensity data, max intensity, analyte id"""
    print("Creating peak list")
    peak_list = []
    peak_id = 1

    for i in range(0, len(raw_import_data[0]), 2):
        # Example header: "556.2771 m/z @3.13 [20200319_GTS_STD_6p25.raw]"
        header_list = raw_import_data[0][i].split(" ")
        mz = float(header_list[0])
        rt = float(header_list[2][1:])
        sample = header_list[3].strip("[").strip("]")
        rt_data = []
        intensity_data = []
        for j in range(2, len(raw_import_data)):
            if (raw_import_data[j][i] != "" and raw_import_data[j][i + 1] != "") and \
                    (raw_import_data[j][i] != "0" and raw_import_data[j][i + 1] != "0"):
                rt_data.append(float(raw_import_data[j][i]))
                intensity_data.append(float(raw_import_data[j][i+1]))
        peak_list.append([sample, peak_id, mz, rt, np.array(rt_data), np.array(intensity_data), max(intensity_data),
                          None])
        peak_id += 1

    return sorted(peak_list, key=itemgetter(6), reverse=True)


def compare_peaks(peak_list):
    """Compare peak shapes between all peaks in the dataset. If relative intensity variation meets match criterion
    group as one analyte. Assign analyte ids"""
    print("Comparing peaks")

    analyte_id = 1
    min_matched_scans = 3
    rsquared_cuttoff = 0.9  # match criterion

    for origin_peak in peak_list:
        if origin_peak[7] is None:
            origin_peak[7] = analyte_id
            for test_peak in peak_list:
                if test_peak[7] is None:
                    matched_rt = sorted(np.intersect1d(origin_peak[4], test_peak[4]))
                    if len(matched_rt) >= min_matched_scans:
                        origin_peak_intensities = []
                        for i, rt in enumerate(origin_peak[4]):
                            if rt in matched_rt:
                                origin_peak_intensities.append(origin_peak[5][i])
                        test_peak_intensities = []
                        for j, test_rt in enumerate(test_peak[4]):
                            if test_rt in matched_rt:
                                test_peak_intensities.append(test_peak[5][j])

                        regression_data = linregress(origin_peak_intensities, test_peak_intensities)

                        # Intensities must vary colinearly if masses are from the same analyte, so r2 must be high.
                        # Relationship must also be positive, so r must be > 0

                        if regression_data.rvalue ** 2 >= rsquared_cuttoff and regression_data.slope > 0:
                            test_peak[7] = analyte_id

            analyte_id += 1

    return peak_list


def export_aligned_peaks(grouped_peak_list, parameters):

    export_data = []

    for row in grouped_peak_list:
        export_data.append([row[0], row[1], row[7], row[2], round(np.average(row[4]), 2)])

    headers = [["sample", "peak_id", "analyte_id", "mz", "rt"]]

    with open (os.path.join(parameters.output_directory, parameters.aligned_peak_output_filename),
               "w", newline='',
               encoding='utf-8') as g:
        csv_g = csv.writer(g)
        csv_g.writerows(headers + export_data)
