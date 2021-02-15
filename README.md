# green_tea_ms
Scripts for mass spectrometry peak alignment for green tea metabolomics project

# Features

This package includes two scripts for mass spectrometry data alignment:

    1) peak_list_align. This tool aligns peak lists for the same sample 
    run on two different instruments. It wirks by first taking retention 
    time and m/z data for a set of standards run on both mass 
    spectrometers and creating a linear regression of these merged data 
    (rt vs rt for each standard) to generate a correction factor to 
    align retention times between instruments. Secondly, it applies this 
    correction to the data from one of the two full peak lists and then 
    identifies peaks within a given retention time and m/z error window 
    that are present in both datasets.
    2) mass_peak_align. This tool deconvolutes mass peaks in a given retention time window to identify adducts, fragments and multiply charged species that derive from the same molecule. 

# Installation Instructions

These scripts require:

Python 3.8
Pandas 1.2.1

To install the scripts:  
    1) clone this GitHub repository locally  
    2) create the following data directories:

    |---green_tea_ms
        |---data
            |---input_data
            |---output_data
    
    3) review the user-editable parameters in execute.py and modify as required
    4) rus as 
'''

python execute.py

'''

# Contributors

Roger Linington: [rlinington](http://github.com/rlinington)