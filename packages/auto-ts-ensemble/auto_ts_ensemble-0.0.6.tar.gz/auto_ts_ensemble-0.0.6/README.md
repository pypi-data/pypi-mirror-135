

# Dependencies 
### Make sure you have install the fbprophet and NeuralProphet
### fbprophet version == 0.7.1
### Steps to install fbprophet
```
conda env -n test_env python==3.8.5
```
```
conda install -c anaconda ephem
```
```
conda install -c conda-forge pystan
```
```
conda install -c conda-forge fbprophet
```

### if error degrade to pystan==2.19.1.1

###Steps to install NeuralProphet
```
pip install neuralprophet ==0.3.0
```

#import
```
from auto_ts_ensemble_rupakbob import auto_ts_ensemble
```

#call the package function 1
```
results = auto_ts_ensemble.neural_analysis(data,freq="H")
```
###access the model
```
neural_prophet = results[0]
```
###access the metrics
```
metrics = results[1]
```
###access the predictions
```
predictions = results[2]
```
####plot the components
```
neural_prophet.plot_components(predictions)
```

#call the package function 2
```
results2 = auto_ts_ensemble.ts_analysis(data,n_future=7)
```
#access the model
```
ts_model = results2[0]
```
#access the predictions
```
predictions2 = results2[1]
```
#plot the components
```
ts_model.plot_components(predictions2)
```

#call the package function 3 ensemble
```
ensemble_predictions = auto_ts_ensemble.ensemble_analysis(predictions,predictions2)
```
