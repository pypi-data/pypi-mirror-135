#Deep_learning-----------------------------
def neural_analysis(data,freq = "D",
                    n_changepoints=10,n_forecasts=7,
                    n_lags = 0, yearly_seasonality="auto",
                    weekly_seasonality='auto',daily_seasonality='auto',
                    batch_size=24,normalize='auto',epochs=100,
                    learning_rate=1.0,impute_missing=True
                    ):
    from neuralprophet import NeuralProphet
    neural_model = NeuralProphet( n_changepoints=n_changepoints,
                      n_forecasts=n_forecasts,
                      n_lags=n_lags,
                      yearly_seasonality=yearly_seasonality,
                      weekly_seasonality=weekly_seasonality,
                      daily_seasonality=daily_seasonality,
                      batch_size=batch_size,
                      normalize=normalize,
                      epochs=epochs,
                      learning_rate=learning_rate,
                      impute_missing=impute_missing)

    metrics =neural_model.fit(data, freq=freq)
        
    future = neural_model.make_future_dataframe(data, periods=n_forecasts, n_historic_predictions=len(data)) #we need to specify the number of days in future
    prediction = neural_model.predict(future)
    
    ### RESIDUALS
    temp1= prediction.iloc[:-n_forecasts,:].reset_index(drop=True)
    ##prediction contains "y" along with yhat1 in neuralprophet
    #thus duplicate error throw
    temp1.drop("y",axis=1,inplace=True)
    temp2 = data["y"].reset_index(drop=True)
    import pandas as pd
    cross_val = pd.concat([temp1,temp2],axis=1)
    cross_val["residuals"] = cross_val["yhat1"]-cross_val["y"] 
    residual_score = cross_val["residuals"].mean(skipna=True)    
    
    prediction["residuals"] = residual_score    
    return neural_model, metrics,prediction;


#------------------------------
#fbprophet
def ts_analysis(data,n_future=7,
                growth='linear',seasonality_mode= 'additive'
                ):
    from fbprophet import Prophet
    ts_model=Prophet(growth= growth,seasonality_mode= seasonality_mode)
    
    ts_model.fit(data)
    ### Create future dates of n days
    #n_future=n_future
    future_dates=ts_model.make_future_dataframe(periods=n_future,freq='H') 
    predictions2=ts_model.predict(future_dates)
    
    ### RESIDUALS
    temp1= predictions2.iloc[:-n_future,:].reset_index(drop=True)
    temp2 = data["y"].reset_index(drop=True)
    import pandas as pd
    cross_val = pd.concat([temp1,temp2],axis=1)
    cross_val["residuals"] = cross_val["yhat"]-cross_val["y"] 
    residual_score = cross_val["residuals"].mean(skipna=True) 
    
    predictions2["residuals"] = residual_score
    return ts_model, predictions2

#ensemble--------------------------
def ensemble_analysis(results1, results2):
    #neural prophet
    df = results1[["yhat1","ds","residuals"]]
    df.rename(columns ={'yhat1':'yhat1','ds':'ds1','residuals':'residual_score1'},inplace=True)

    #fbprophet
    df1 = results2[["yhat","ds","residuals"]]
    df1.rename(columns ={'yhat':'yhat2','ds':'ds1','residuals':'residual_score2'},inplace=True)

    import pandas as pd
    df_2 = pd.concat([df,df1],axis=1)
    df_2["yhat_Average"] = df_2[["yhat1","yhat2"]].mean(axis=1)
    df_2["Residual_Score_Average"] = df_2[["residual_score1","residual_score2"]].mean(axis=1)

    return df_2