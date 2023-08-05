from requests.api import options
from mmanager.mmanager import Model
secret_key = '9cb2825b932f33e40556de3dfd415c0f395503e5'
url = 'http://localhost:8000'
path = 'assets'

model_data = {
    "project": 46,
    "transformerType": "Classification",
    "training_dataset": "/home/mizal/Desktop/histo/histo_train-1.csv",
    "test_dataset": "/home/mizal/Desktop/histo/histo_test.csv",
    "pred_dataset": "/home/mizal/Desktop/histo/histo_pred.csv",
    "actual_dataset": "/home/mizal/Desktop/histo/histo_truth.csv",
    "model_file_path": "/home/mizal/Desktop/histo/histo_model.h5",
    "target_column": "label",
    "note": "API TESTTTTTT",
}

Model(secret_key, url).post_model(model_data)
