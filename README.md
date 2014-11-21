SensorDataResearchReproduction
==============================

Project homepage: [https://osf.io/q8f9t/](https://osf.io/q8f9t/)

Note: The IBRL Dataset used in this project can be located here: [http://db.lcs.mit.edu/labdata/labdata.html](http://db.lcs.mit.edu/labdata/labdata.html)

###Quickstart Guide

Welcome, this quickstart guide will help you get your environment set up and your IPython notebook server up and running.

1. Clone the GitHub Repository:
  
  ```bash
  $ git clone https://github.com/HarryRybacki/SensorDataResearchReproduction.git
  Cloning into 'SensorDataResearchReproduction'...
  ...
  Resolving deltas: 100% (53/53), done.
  Checking connectivity... done.
  
  $ cd SensorDataResearchReproduction
  ```
2. (Recommended optional step) Create a new virtual environment for this repository (I'm using virtualenvwraper but you can use whatever):
  
  ```bash
  $ mkvirtualenv sensorwork
  New python executable in sensordata/bin/python2.7
  Also creating executable in sensordata/bin/python
  Installing setuptools, pip...done.
  ```
3. Install the Python requirements:

  ```bash
  (sensordata)...$ pip install -r requirements.txt
  Downloading/unpacking Jinja2==2.7.3 (from -r requirements.txt (line 1))
  ...
  Successfully installed Jinja2 MarkupSafe backports.ssl-match-hostname certifi gnureadline ipython matplotlib mock nose numpy pyparsing python-dateutil pytz pyzmq six tornado
  Cleaning up...
  ```
4. Launch the IPython Notebook server:

  ```bash
  (sensordata)...$ ipython notebook
  ...[NotebookApp] Using existing profile dir: u'/Users/hrybacki/.ipython/profile_default'
  ...[NotebookApp] Using MathJax from CDN: https://cdn.mathjax.org/mathjax/latest/MathJax.js
  ...NotebookApp] The port 8888 is already in use, trying another random port.
  ...[NotebookApp] Serving notebooks from local directory: /Users/hrybacki/git/test/SensorDataResearchReproduction
  ...[NotebookApp] 0 active kernels 
  ...[NotebookApp] The IPython Notebook is running at: http://localhost:8888/
  ...[NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
  ```
At this point the IPython notebook server should have automatically re-directed your machine to the default browser and opened the main view of the IPython notebook server (in the sample output above this is: **http://localhost:8888/**). From this screen you can view the directory structure of the project as well as any IPython notebooks that are present. 

5. Open the IPython notebook:
  Simply click the **AnomalyDetectionNotebookV2.ipynb** link and the notebook will open and you are ready to get started!
