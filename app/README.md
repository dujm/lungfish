[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)
------
## X-Ray Vision Web Application
### I. The currently supported functions


#### 1. Online app
  * Go to http://18.185.53.230:8050
  * Visualization of Registered Medical Images
    * Check metadata of DICOM files
    * Visualization of DICOM files  

  * Summary Graphs of Registered Medical Images
  * Note: a Pneumonia sample dataset is used in the demo (1000 DICOM files)

<br>

#### 2. Local Medical Image Visualization
  * 1) Preparation
```
  # Open your terminal and clone the repository  
    git clone https://github.com/oceanprotocol/lungfish.git
  # Copy your DICOM (.dcm) files to 'localpathto/lungfish/app/  data/local_image/'
  # Run the app in your terminal
    cd lungfish/app
    pip install -r requirements.txt
    python index.py
```

  * 2) Visualization
   * Go to http://127.0.0.1:8050/ in your browser
   * Click the tab 'Local Image Processing'
   * The metadata of all your local dcm files are automatically summarized in the table
   * Click a row and visualize a DICOM file

  <br>

### III. Built with
  * Dash - Main server and interactive components
  * Plotly Python - Used to create the interactive plots

![Screenshot](https://raw.githubusercontent.com/oceanprotocol/lungfish/develop/app/X_Ray_Vision.png)

<br>

### IV. Reference  
[dash-salesforce-crm](https://github.com/plotly/dash-salesforce-crm)
