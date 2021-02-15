# green_tea_ms
Scripts for mass spectrometry peak alignment for green tea metabolomics project

# Features

This package includes two scripts for mass spectrometry data alignment:

    1. peak_list_align. This tool aligns peak lists for the same sample run on two different instruments. It wirks by first taking retention time and m/z data for a set of standards run on both mass spectrometers and creating a linear regression of these merged data (rt vs rt for each standard) to generate a correction factor to align retention times between instruments. Secondly, it applies this correction to the data from one of the two full peak lists and then identifies peaks within a given retention time and m/z error window that are present in both datasets.
    2. mass_peak_align. This tool deconvolutes mass peaks in a given retention time window to identify adducts, fragments and multiply charged species that derive from the same molecule. 

# Installation Instructions

These scripts require:

- Python 3.8
- Pandas 1.2.1

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

##  peak_list_align

This script requires three input files:

    1. __Standards List:__ A csv file containing three columns: standard_name, lab_1_rt, lab_2_rt. 
        - Filename is standards.csv
        - standards_name is a string of the name of the standard. 
        - lab_1_rt and lab_2_rt are the retention times (in minutes) of the standard from each laboratory. 
    2. **Laboratory 1 Feature List:** A csv file containing two columns: feature_rt and feature_mz.
        - Filename is lab_1_feature_list.csv
        - This is the feature list from the test sample from Laboratory 1. 
        - Typically derived from MZMine 2, although it will work with feature lists from any MS processing software provided that rt and m/z values are generated.
    3. **Laboratory 2 Feature List:** A matching feature list for the same sample analyzed in Laboratory 2. 
        - Filename is lab_2_feature_list.csv
        - Requires the same structure as Laboratory 1 feature list. 

## mass_peak_align

This script requires one input file containing four columns: peak_id, scan, mz, intensity:

    - Filname is mass_peak_scan_data.csv
    - 
# Contributors

Roger Linington: [rlinington](http://github.com/rlinington)