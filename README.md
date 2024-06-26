# House Price Prediction System

This repository contains   **House Price Prediction System**. This application is designed to provide users to predict prices of houses.


### System Requirements

1. Python 
2. pip


### 1. Clone the repository:

``` bash
git clone https://github.com/Sahan-g/House-Price-Prediction--H2O-.git
```

### 2. Create a virtual environment:

``` bash
python -m venv venv
```

### 3. Activate the virtual environment:
``` bash
source venv/bin/activate
```

**windows**
``` bash
venv\Scripts\activate.bat
```
To deactivate the virtual environment use ```deactivate``` command.

### 4. Install dependencies:

``` bash
(venv) pip install -r requirements.txt 
```

### 5. Run the app:
``` bash
(venv) wave run application.py
```

### 6. View the app:
from any brower open http://localhost:10101/housepriceprediction


### Training the model using AutoML

``` bash
(venv) python model.py
```


## Model Performance Evaluation

ModelMetricsRegressionGLM: stackedensemble
** Reported on test data. **


MSE: 2520067301.7079897 <br>
RMSE: 50200.27192862594 <br>
MAE: 40055.82609704756 <br>
RMSLE: NaN <br>
Mean Residual Deviance: 2520067301.7079897 <br>
R^2: 0.5659614664184998 <br>
Null degrees of freedom: 9954 <br>
Residual degrees of freedom: 9944 <br>
Null deviance: 57800097145507.875 <br>
Residual deviance: 25087269988503.04 <br>
AIC: 243776.4408324747 <br>


**Preview**

Watch preview on YouTube : [youtube](https://youtu.be/xfz9_EO-cFI) 



**Sources**

H2O Wave, check out the [Wave](https://wave.h2o.ai/).

H2O AutoML, check out the [AutoML](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/automl.html).

Thank you
