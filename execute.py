#!/usr/bin/env python3

"""Tools for aligning mass spectrometry datasets between laboratories"""

import os
import csv
import sys
from operator import itemgetter

from peak_alignment import feature_list as feature_list
from peak_alignment import peak_list as peak_list


class Parameters:
    """Class containing all of the setup parameters from green_tea_ms"""
    def __init__(self):
        self.input_directory = os.path.join("data", "input_data")
        self.peak_scan_lab_a_filename = "standards_lab_a_mass_peak_scan_data.csv"
        self.peak_scan_lab_b_filename = "standards_lab_b_mass_peak_scan_data.csv"
        self.standards_filename = "standards_rt_data.csv"
        self.lab_a_features_filename = "laboratory_a_feature_list.csv"
        self.lab_b_features_filename = "laboratory_b_feature_list.csv"
        self.output_directory = os.path.join("data", "output_data")
        self.lab_a_aligned_peak_output_filename = "lab_a_aligned_peak_list.csv"
        self.lab_b_aligned_peak_output_filename = "lab_b_aligned_peak_list.csv"
        self.aligned_feature_output_filename = "aligned_feature_list.csv"
        self.rt_error = 0.1
        self.mz_da_error = 0.05
        self.standards_slope = None
        self.standards_intercept = None


def peak_list_align(parameters):
    """Import a csv file containing scan by scan peak data from MZMine 2 and deconvolute to individual analytes based
    on peak shape alignment

    """

    for dataset in [(parameters.peak_scan_lab_a_filename, parameters.lab_a_aligned_peak_output_filename),
                    (parameters.peak_scan_lab_b_filename, parameters.lab_b_aligned_peak_output_filename)]:
        raw_import_data = []
        with open(os.path.join(parameters.input_directory, dataset[0]), encoding='utf-8') as f:
            csv_f = csv.reader(f)
            for row in csv_f:
                raw_import_data.append(row)

        raw_peak_list = peak_list.create_peak_list(raw_import_data)
        grouped_peak_list = peak_list.compare_peaks(raw_peak_list)
        peak_list.export_aligned_peaks(grouped_peak_list, parameters, dataset[1])


def feature_list_align(parameters):
    """Align LCMS data on the same sample set from two different instruments using rt and mz matching, and an rt
    correction factor based on standards rt values from both instruments

    """
    standards_rt_data = []
    with open(os.path.join(parameters.input_directory, parameters.standards_filename), encoding='utf-8') as g:
        csv_g = csv.reader(g)
        for row in csv_g:
            standards_rt_data.append([row[0], float(row[1]), float(row[2])])

    parameters.standards_slope, parameters.standards_intercept = feature_list.standards_relationship(standards_rt_data)

    lab_a_data = []
    with open(os.path.join(parameters.input_directory, parameters.lab_a_features_filename), encoding='utf-8') as h:
        csv_h = csv.reader(h)
        next(h)
        for row in csv_h:
            # insert mz and rt data to list. Add third column (default None) to track whether peak is already matched to
            # a feature from laboratory B
            lab_a_data.append([float(row[0]), float(row[1]), None])
    sorted_lab_a_data = sorted(lab_a_data, key=itemgetter(0))

    lab_b_data = []
    with open(os.path.join(parameters.input_directory, parameters.lab_b_features_filename), encoding='utf-8') as i:
        csv_i = csv.reader(i)
        next(i)
        for row in csv_i:
            # insert mz and rt data to list
            lab_b_data.append([float(row[0]), float(row[1])])
    sorted_lab_b_data = sorted(lab_b_data, key=itemgetter(0))

    feature_list.align_ms_features(sorted_lab_a_data, sorted_lab_b_data, parameters)


if __name__ == "__main__":

    parameters = Parameters()
    selected_analysis = input("Select required analysis (1 or 2). 1 = peak alignment, 2 = feature alignment: ")

    if selected_analysis == "1":
        peak_list_align(parameters)
    elif selected_analysis == "2":
        feature_list_align(parameters)
    else:
        print("Invalid selection")
        sys.exit()
