from model import predict_batch
import h2o

h2o.init()
model = h2o.load_model('./saved_models/StackedEnsemble_BestOfFamily_1_AutoML_3_20240521_131303')

predict_batch(model,'./batch.csv')