## X-Ray Vision App

### Built With
  * Dash - Main server and interactive components
  * Plotly Python - Used to create the interactive plots


### I.What functions are included in the online app?

##### 1. Image Asset Visualisation
  * Check metadata of DICOM files
  * Visualization of DICOM files  

##### 2. Image Asset Summary: Summary graphs of the sample dataset  
##### Sample Size: A Pneumonia Sample Dataset (1000 medical images in DICOM format )

<br>

###  II. How to run the app locally?
##### 1. Open your terminal and clone the repository  

```
  git clone https://github.com/oceanprotocol/lungfish.git
```  
##### 2. copy your DICOM (.dcm) files in "lungfish/app/data/local_image/" directory
##### 3. Run the below commands in your terminal

```    
    cd lungfish/app
    pip install -r requirements.txt
    python index.py
```

##### 4. Go to "http://127.0.0.1:8050/" in your browser
##### 5. Click the tab "Local Image Processing"
  * The meta data of all your local dcm files are automatically summarized in the table
  * Click a row and visualize a DICOM file



### Screenshots
!
