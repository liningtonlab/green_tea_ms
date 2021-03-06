# green_tea_ms
Scripts for mass spectrometry peak alignment for green tea metabolomics project

# Features

This package includes two scripts for mass spectrometry data alignment:

feature_list_align. This tool aligns feature lists for the same sample run on two different instruments. It works by first taking retention time and m/z data for a set of standards run on both mass spectrometers and creating a linear regression of these merged data (rt vs rt for each standard) to generate a correction factor to align retention times between instruments. Secondly, it applies this correction to the data from one of the two full peak lists and then identifies peaks within a given retention time and m/z error window that are present in both datasets.
mass_peak_align. This tool deconvolutes mass peaks in a given retention time window to identify adducts, fragments and multiply charged species that derive from the same molecule.

# Installation Instructions

These scripts require:

- Python 3.8
- pandas 1.2.1
- scipy 1.6.0
- numpy 1.19.2

To install the scripts:

    1. clone this GitHub repository locally
    2. create the following data directories in the green_tea_ms repo directory:
        
            |---green_tea_ms
                |---data
                    |---input_data
                    |---output_data

    3. review the user-editable parameters in execute.py (lines 17 - 28) and modify as required
    4. run as:

```
python execute.py
```

# Input Data

##  feature_list_align

This script requires three input files:

    1. Standards List: A csv file containing three columns: standard_name, lab_A_rt, lab_B_rt. 
        - Filename is standards_rt_data.csv
        - File should not contain any headers (i.e. first row should be data, not column headings)    
        - standards_name is a string of the name of the standard. 
        - lab_A_rt and lab_B_rt are the retention times (in minutes) of the standard from each laboratory. 
    2. Laboratory A Feature List: A csv file containing two columns: feature_rt and feature_mz.
        - Filename is laboratory_a_feature_list.csv
        - First row should be column headers. NOTE: First row is skipped, so must not contain data.    
        - This is the feature list from the test sample from Laboratory A. 
        - Typically derived from MZMine 2, although it will work with feature lists from any MS processing software provided that rt and m/z values are generated.
    3. Laboratory B Feature List: A matching feature list for the same sample analyzed in Laboratory B. 
        - Filename is laboratory_b_feature_list.csv
        - Requires the same structure as Laboratory B feature list. 

## mass_peak_align

This script requires two input files; the exported peak list files from each laboratory processed in MZmine 2:

    - Filnames are standards_lab_a_mass_peak_scan_data.csv and standards_lab_b_mass_peak_scan_data.csv
    - Files are generated as follows: Upon completing MZmine processing double-click on the aligned feature list to open the detailed feature window. Next use "Ctrl+A" to select all features, right-click and chose "show" and then "XIC (base peak)".  This will reveal a chromatogram of all features. Right-click on the chromatogram and select "export data" to excel to produce the scan by scan dataset for all features.

# Script Functions

## feature_list_align

This script first defines a correction factor to align feature retention times between instruments. This is required because of small differences in the UPLC flow paths that lead to subtle differences in retention times between instruments. To determine this correction, standards are run on each instrument and a linear regression determined for a plot of rt vs rt for each standard. From the slope and intercept of this plot (determined by feature_list.standards_relationship) it is possible to correct all the rt values from one instrument so that they align with the other. This is performed by the feature_list.rt_match function.
After rt correction, features are considered a match if they are within a defined m/z and rt window of a matching feature from the other dataset. This dataset alignment is performed by feature_list.align_mass_features which exports a csv containing the feature list from laboratory A, matching features from Laboratory B, and a True/False match flag column.

## mass_peak_align

This script groups m/z features that derive from the same molecule based on relative intensity variations across the retention time scale. peaks that derive from the same molecule (e.g. different adducts, fragments etc) must vary colinearly, given that intensity is proportional to concentration within the linear response range of the detector. Peaks with matching peak shapes (i.e. the same relative intensity variation as a function of time) are asigned an analyte ID and annotated as belonging to the same compound. This is performed by determining the r-squared value for the linear regression of intensity vs intensity on a per scan basis for each pair of overlapping peaks.

# Contributors

Roger Linington: [rlinington](http://github.com/rlinington)