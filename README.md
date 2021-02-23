# green_tea_ms
Scripts for mass spectrometry peak alignment for green tea metabolomics project

# Features

This package includes two scripts for mass spectrometry data alignment:

    1. feature_list_align. This tool aligns feature lists for the same sample run on two different instruments. It wirks by first taking retention time and m/z data for a set of standards run on both mass spectrometers and creating a linear regression of these merged data (rt vs rt for each standard) to generate a correction factor to align retention times between instruments. Secondly, it applies this correction to the data from one of the two full peak lists and then identifies peaks within a given retention time and m/z error window that are present in both datasets.
    2. mass_peak_align. This tool deconvolutes mass peaks in a given retention time window to identify adducts, fragments and multiply charged species that derive from the same molecule. 

# Installation Instructions

These scripts require:

- Python 3.8
- pandas 1.2.1
- scipy 1.6.0

To install the scripts:

    1. clone this GitHub repository locally
    2. create the following data directories:
        
            |---green_tea_ms
                |---data
                    |---input_data
                    |---output_data

    3. review the user-editable parameters in execute.py and modify as required
    4. run as:

```
python execute.py
```

# Input Data

##  feature_list_align

This script requires three input files:

    1. __Standards List:__ A csv file containing three columns: standard_name, lab_A_rt, lab_B_rt. 
        - Filename is standards.csv
        - standards_name is a string of the name of the standard. 
        - lab_A_rt and lab_B_rt are the retention times (in minutes) of the standard from each laboratory. 
    2. **Laboratory A Feature List:** A csv file containing two columns: feature_rt and feature_mz.
        - Filename is lab_a_feature_list.csv
        - This is the feature list from the test sample from Laboratory A. 
        - Typically derived from MZMine 2, although it will work with feature lists from any MS processing software provided that rt and m/z values are generated.
    3. **Laboratory B Feature List:** A matching feature list for the same sample analyzed in Laboratory B. 
        - Filename is lab_b_feature_list.csv
        - Requires the same structure as Laboratory B feature list. 

## mass_peak_align

This script requires one input file; the exported peak list file from MZmine 2:

    - Filname is mass_peak_scan_data.csv
    - 
# Contributors

Roger Linington: [rlinington](http://github.com/rlinington)