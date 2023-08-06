
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5523256.svg
   :target: https://doi.org/10.5281/zenodo.5523256

SampleSlicer
============
SampleSlicer is a tool written in python designed to enable the transformation
of arbitrary 3D or 4D datasets loaded as a set of image stacks. SampleSlicer was
initially designed for use in a scientific experiment involving time-series
X-ray computed tomography (XCT) images which contain multiple independent
specimens (microtubes) embedded in a single experimental dataset. The tool
provides a GUI for drawing rectangles bounding the tubes at specified slices and
time points. Information about the rectangle location and orientation in space
and time is used to crop, align and rotate each individual microtube and
ultimately create 4D hyperstacks of each tube for enhanced data exploration and
analysis.

Why SampleSlicer?
-----------------
Modern datasets are very large and the process of parsing them for analysis
requires a significant amount of computation. Current tools may struggle to
perform this task in an efficient way.

The primary goal of SampleSlicer is to split up a large 4-dimensional dataset
into smaller samples using a graphical interface for defining the "tubes" of
data which may require cropping and rotation in 3D. After the data has been
cropped, aligned and rotated, it may be saved as sets of image sequences or as a
4D hyperstack compatible with ImageJ.

Once this "slicing" is complete, ImageJ can be used to view the sub-samples with
the hyperstack viewer or as individual images or image sequences on which
analysis can be performed.

How does SampleSlicer work?
---------------------------
SampleSlicer performs 3D rotations in an efficient way by computing a single
rotation matrix using quaternions which allows the transformation to be done
using a single multiplication operation rather than a series of euclidean
transformations. This allows the transformation to handle pitch, yaw, and roll
without the risk of gimbal locking.

SampleSlicer may also load a subset of data for the purposes of generating
rotation metadata, allowing very large datasets to be considered without loading
all of the data into memory. 

Installing
----------
SampleSlicer may be run in an anaconda environment or any other virtual
environment.

Installing from PyPI:

.. code:: bash

  pip install sampleslicer

Installing from source (e.g. Zenodo archive):

.. code:: bash
  
  unzip sampleslicer-1.0.0.zip
  cd sampleslicer-1.0.0
  pip install .

Dependencies
~~~~~~~~~~~~
SampleSlicer is compatible with python3 with dependencies installed
automatically using pip via requirements.txt:

- matplotlib
- numpy
- numpy-quaternion
- scipy
- imread
- psutil

System utilities:

- LibTIFF
  
  - Used for updating tiff metadata for ImageJ compatible hyperstacks. Can be
    obtained from https://libtiff.gitlab.io/libtiff/.
  - May be installed through cygwin installer, `apt install libtiff5` on
    Debian/Ubuntu, etc and must be available on the system PATH.

- bash

  - calls to the tiffcp utility currently assume a bash environment (such as
    anaconda / cygwin or Linux, etc.)

Running
-------
Successful use of SampleSlicer consists of two phases: 1) generation of
transformation metadata via GUI 2) batch processing which performs data
transformation and writes image sequences and hyperstacks.

An optional third step is to generate stacks at a given slice vs. time, which is
useful for movie making and for datasets that are too large to be saved as a
hyperstack. (Hyperstacks can be no larger than 4 GB.)

Project setup
~~~~~~~~~~~~~
Once the SampleSlicer package is installed copy the template files `sliceit.py`
and 'slicetimestack.py' to the directory where the package has been installed
and the analysis is being performed. 'sliceit.py' is used to generate
transformation metadata and batch process the data, and 'slicetimestack.py' is
used to generate stacks at a given slice vs. time (only after batch processing
using 'sliceit.py' is complete).  

Generate SampleSlicer script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Use the following command to generate script templates (`sliceit.py` and
`slicetimestack.py`) in current directory.

.. code:: bash

  mkdir sliceit_project
  cd sliceit_project
  sslice -g
  
Verify input data file and directory structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SampleSlicer will work with any data as long as the samples and files are named
sequentially and hierarchically as described below:

.. parsed-literal::

    assumes a sample directory of:
            - sample0_time0
                - slice0
                - slice1
                ...
                - sliceN
            - sample0_time1
                - slice0
                - slice1
                ...
                - sliceN
            ...
            - sample0_timeN
                - slice0
                - slice1
                ...
                - sliceN

            - sample1_time0
                - slice0
                - slice1
                ...
                - sliceN
            - sample1_time1
                - slice0
                - slice1
                ...
            ...
            - sample1_timeN
                - slice0
                - slice1
                ...
                - sliceN

Customize the script for your dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A few variables need to be set up one time to point to the dataset and to tell
SampleSlicer how to interpret the images.  Note that these paths may need to
change if you move your dataset.

At minimum set the variables `sample0_path`, `sample0_pat`, and `sample0_img` to
point to your dataset. The image files must be numbered or ordered in the
spatial and time sequence in which they are to be interpreted.

The `sub_sample` option is used to only open a portion of a very large dataset.
This value should not be set to a value larger than the total number of slices.

The asterisk (*) below is used to select specific patterns of files in the input
directories and must only match the samples and image files being processed.

.. code:: python

  #
  # Dataset configuration options
  #

  # path information for our sample set
  sample0_path = "H:\Microtubes_all\Recons2"
  sample0_pat = "rec201611*"
  sample0_img = "*.tiff"

Configure the `output_path` variable to be the location of the microtubes file
and the generated sliced datasets (after batch processing). SampleSlicer
*should* never modify anything outside of the `output_path` directory but it is
recommended to make this a different path from the input dataset.

.. code:: python

  # this is the filename used for reading and writing microtube definitons in the
  # editor. when performing batch processing this is the file that will define
  # the regions for the microtubes.
  microtubes_json = "microtubes.json"

Interactive metadata generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SampleSlicer includes a GUI which allows for the specification of a complex
transformation. To run the SampleSlicer editor for browsing and generating the
metadata use the following command:

.. code:: python
  
  sslice --editor

Interactive commands for generation of transformation metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The transformation metadata is generated by drawing rectangles on each end of
the tube at different time points in the dataset. The rectangles represent the
3D space containing the microtube. This procedure may be performed using a GUI
provided in this package. The hotkeys used to manipulate the rectangles and
other aspects of the GUI are defined below.


Hotkeys
'''''''
  1. Translate:

    a. large jump: hjkl. (e.g., use "h", "j", "k" and "l" keys to move
       the rectange in the x and y directions in large jumps)
    b. small jump (1 pixel): arrow keys

  2. Rotate: m,./
  3. Contract/expand: yuio
  4. Write: w
  5. New rectangle: N
  6. Extract: e
  7. Send rect to background: b
  8. Switch between display and edit mode: esc
  9. Print: p
  10. Go to first slice: "Home"
  11. Go to last slice: "End"

Procedure for drawing rectangles
''''''''''''''''''''''''''''''''
This is an example of the procedure for creating the sets of rectangles.

Procedure for one tube:
1. Go to center time using scroll bar.

  a. Draw rectangle for first slice -- get it perfectly centered and rotated and
  sized.
  b. Go to last slice. Translate rectangle as needed to center it. Make sure the
  rectangle is big enough to contain entire tube.

2. Go to time 0, first slice: Expand rectangle to include entire tube (DO NOT
   ROTATE OR TRANSLATE RECTANGLE)
3. Go to time 0, last slice: Expand rectangle to include entire tube (DO NOT
   ROTATE OR TRANSLATE RECTANGLE)
4. Go to time N, first slice: Expand rectangle to include entire tube (DO NOT
   ROTATE OR TRANSLATE RECTANGLE)
5. Go to time N, last slice: Expand rectangle
   to include entire tube (DO NOT ROTATE OR TRANSLATE RECTANGLE)
6. Write (w) data.

To generate metadata for the next tube, use the "N" hotkey to make a new rectangle. 

Batch mode
~~~~~~~~~~
Run with `batch = True` to produce output data including folders of rotated data
in the 'x' and 'z' directions and hyperstacks. This data is written out to the
`output_dir` along with a log of the batch processing operations performed.

.. code:: bash

  sslice --batch

Output visualization
~~~~~~~~~~~~~~~~~~~~
SampleSlicer has the ability to include metadata to generate ImageJ-compatible
hyperstacks of the output datasets. By default, 4D hyperstacks of each
"microtube" are output and can be opened in ImageJ. If the output dataset is too
large for the hyperstack format (>4 GB), the hyperstack will not be complete and
cannot be opened in ImageJ.

The included script `slicetimestack.py` may be used to make stacks at a given
slice vs. time which is useful for movie making and for datasets that are too
large to be saved as a hyperstack.

To achieve this copy the script from the utils directory and configure it to
point at the output dataset after the complete batch run has been performed.
Set the parameters for the slices to generate and invoke the script as follows:

.. code:: bash

  python slicetimestack.py

Implementation details
----------------------

Metadata format
~~~~~~~~~~~~~~~
The metadata for each region of interest is defined using the data required to
specify an end-to-end sub-region of the sample. The region defines a 3d skewed
polygon which is used to compute the rotation.

This is represented using:

  - pt0: centroid point at image0
  - pt1: centroid point at imageN
  - angle: the angle of rotation of each of the rectangles
  - width: width of both of the rectangles
  - height: height of both of the rectangles

.. code:: json

   "00": {
        "angle": 66.80000000000018, 
        "height": 111.17145539604599, 
        "pt0": [
            41.8898228635052, 
            1695.266508580275
        ], 
        "pt1": [
            77.8898228635052, 
            1669.266508580275
        ], 
        "width": 278.9356472920259
    }, 

Copyright and License
---------------------
SampleSlicer is licensed under the GPLv3 license.
Copyright (C) 2018-2022 John W. Williams

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.

