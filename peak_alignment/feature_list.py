#!/usr/bin/env python3

import os
import csv
from scipy.stats import linregress


def mass_match(mass1, mass2, parameters):
    """Assess peak match based on mz values and Da mz error"""

    if mass1 - parameters.mz_da_error <= mass2 <= mass1 + parameters.mz_da_error:
        return True
    else:
        return False


def rt_match(rt1, rt2, parameters):
    """Assess peak match based on rt values and rt error"""

    corrected_rt1 = (rt1 - parameters.standards_intercept) / parameters.standards_slope

    if corrected_rt1 - parameters.rt_error <= rt2 <= corrected_rt1 + parameters.rt_error:
        return True
    else:
        return False


def standards_relationship(standards_list):
    """Determine slope and intercept for plot of rt vs rt for standards from laboratories A and B"""

    lab_a_rt = []
    lab_b_rt = []

    for row in standards_list:
        lab_a_rt.append(float(row[1]))
        lab_b_rt.append(float(row[2]))

    linear_regression = linregress(lab_b_rt, lab_a_rt)
    print("Standards calibration regression. Slope: " + str(linear_regression.slope) + " Intercept: "
          + str(linear_regression.intercept))

    return round(linear_regression.slope, 3), round(linear_regression.intercept, 4)


def align_ms_features(lab_a_data, lab_b_data, parameters):
    """Compare feature lists from two different instruments and identify features that match between the two lists,
    within defined mz and rt error windows

    """

    for lab_b_peak in lab_b_data:
        peak_match = False
        for lab_a_peak in lab_a_data:
            if not lab_a_peak[2]:
                if mass_match(lab_b_peak[0], lab_a_peak[0], parameters) and rt_match(lab_b_peak[1], lab_a_peak[1],
                                                                                     parameters):
                    lab_b_peak.append(lab_a_peak[0])
                    lab_b_peak.append(lab_a_peak[1])
                    lab_b_peak.append(True)
                    peak_match = True
                    lab_a_peak[2] = True
                    break
        if not peak_match:
            lab_b_peak.append(None)
            lab_b_peak.append(None)
            lab_b_peak.append(False)

    headers = [["Laboratory_B_mz", "Laboratory_B_rt", "Laboratory_A_mz", "Laboratory_A_rt", "Matched"]]

    with open(os.path.join("data",
                           "output_data",
                           parameters.aligned_feature_output_filename), "w", newline='') as k:
        csv_k = csv.writer(k)
        csv_k.writerows(headers + lab_b_data)

    print("Total number of features from Laboratory A: " + str(len(lab_a_data)))
    print("Total number of features from Laboratory B: " + str(len(lab_b_data)))

    lab_a_match_count = 0
    for row in lab_a_data:
        if row[2]:
            lab_a_match_count += 1
    print("Number of Laboratory A matched features = " + str(lab_a_match_count))

    lab_b_match_count = 0
    for row in lab_b_data:
        if row[4]:
            lab_b_match_count += 1
    print("Number of Laboratory B matched features = " + str(lab_b_match_count))
