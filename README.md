


[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

### X-Ray Vision Medical Diagnostics Workflow

> A healthcare use case, powered by [Ocean](https://oceanprotocol.com).

------

## Table of Contents
- [Blog](#blog)
- [Features](#features)
- [Files](#files)
- [Prerequisites](#prerequisites)
- [Code style](#code-style)
- [New Version](#new-version)
- [License](#license)
------
## Blog
  * [Blog Post in English](https://blog.oceanprotocol.com/x-ray-vision-a-healthcare-use-case-d18ea64bdd2b)
  * [Blog Post in simplified Chinese](https://medium.com/ocean-protocol-international/x-ray-vision-%E6%99%BA%E6%85%A7%E5%8C%BB%E7%96%97%E7%9A%84%E5%BA%94%E7%94%A8%E6%A1%88%E4%BE%8B-2007918df2cc)

## Features
The major modules in X-Ray Vision are

  * Medical Image Visualization App
    * https://x-ray-vision.herokuapp.com

  * Lung Opacity Detection using Deep Learning
    * Check [Jupyter Notebooks](https://github.com/oceanprotocol/lungfish/tree/develop/ocean_assets/notebook)

##  Files
    ├── requirements.txt : packages
    ├── app: I. Medical Image Visualization (Web-application)
    ├── ocean_assets: II. Lung Opacity Detection using Deep Learning
    │   ├── image_data
    │   ├── meta_data
    │   ├── models
    │   ├── notebook
    │   ├── utils
    │   └── visualization
    ├── references
    ├── reports: More data Visualization
    ├── src: Source files
    │   ├── Mask_RCNN: Mask_RCNN library
    │   ├── config: functions
    └── └── data: raw data and processed data (image data is not uploaded to GitHub)

## Prerequisites
    Python 3


## Code style
The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md) and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).
    ​    

## New Version
The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.


## License
```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");nyou may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

```
