import pandas as pd 
import h2o
from h2o.automl import H2OAutoML

def train_model ():

    '''
    Train H2O AutoML model on house prices
    After the initilization of H2o instance, loads the dataset,
    then perform preprocessing and train the model


    No Arguments and does not return anything

    '''
    h2o.init()

    df = h2o.import_file(path='./dataset/housing_price_dataset.csv')

    x= df.columns
    y= "Price"

    x.remove(y)

    train_set, test_set = df.split_frame(ratios=[0.8],seed=1)

    aml= H2OAutoML(max_models=20,seed=1,max_runtime_secs=3600)
    aml.train(x=x,y=y,training_frame=train_set,leaderboard_frame=test_set)

    best_model = aml.leader
    model_path = h2o.save_model(model=best_model, path="./saved_models", force=True)
    print(f"Model saved to: {model_path}")
    pred = best_model.model_performance(test_set)
    print(pred)
    



def predict(model, params):
   
    '''
    Predict the price of a house according to given data

    Arguments - model and dictinary object that contains the prediction parameter data


    Returns - Predicted price
   
    '''

    input_df = pd.DataFrame([params])
    input_h2o_df = h2o.H2OFrame(input_df)

    prediction = model.predict(input_h2o_df)
    with h2o.utils.threading.local_context(polars_enabled=True, datatable_enabled=True):
        prediction_df = prediction.as_data_frame()

    response = prediction_df.iloc[0].tolist()
    print(response)

    return response[0] 
    


def predict_batch(model,file_path):
    
    '''
    This function predicts the prices for all the rows of the uploaded csv file

    Arguments -  model and the path of the csv file
    
    '''
    data_df = pd.read_csv(file_path)

   
    data_h2o_df = h2o.H2OFrame(data_df)

    
    predictions = model.predict(data_h2o_df)
    with h2o.utils.threading.local_context(polars_enabled=True, datatable_enabled=True):
        predictions_df = predictions.as_data_frame()

   
    print(predictions_df)
    return predictions_df

if __name__ =='__main__':
    train_model()
