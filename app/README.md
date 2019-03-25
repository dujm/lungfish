[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)
------
## X-Ray Vision Web Application
### I.The currently supported functions
Go to http://18.185.53.230:8050

#### 1.Visualisation of Registered Medical Images
  * Check metadata of DICOM files
  * Visualization of DICOM files  

#### 2. Summary graphs of Registered Medical Images
##### For demo: A Pneumonia sample dataset is used (1000 DICOM files)

<br>

###  II. How to run the app locally for sensitive data?
#### 1. Open your terminal and clone the repository  

```
  git clone https://github.com/oceanprotocol/lungfish.git
```  
#### 2. Copy your DICOM (.dcm) files to 'lungfish/app/data/local_image/'

#### 3. Run the below commands in your terminal

```    
  cd lungfish/app
  pip install -r requirements.txt
  python index.py
```

#### 4. Go to http://127.0.0.1:8050/ in your browser
#### 5. Click the tab 'Local Image Processing'
  * The meta data of all your local dcm files are automatically summarized in the table
  * Click a row and visualize a DICOM file

  <br>

### III. Built With
  * Dash - Main server and interactive components
  * Plotly Python - Used to create the interactive plots

![Screenshot](https://raw.githubusercontent.com/oceanprotocol/lungfish/develop/app/X_Ray_Vision.png)

<br>

### IV. Blog  
[Blog Post on Medium](https://blog.oceanprotocol.com/)

<br>
### V. Reference  
[dash-salesforce-crm](https://github.com/plotly/dash-salesforce-crm)
