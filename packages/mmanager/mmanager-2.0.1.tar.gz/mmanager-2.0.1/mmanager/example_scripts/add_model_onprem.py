from mmanager.mmanager import Model
secret_key = '9cb2825b932f33e40556de3dfd415c0f395503e5'
url = 'http://localhost:8000'
path = 'assets' #path to csv file
model_data = {
    "project": 46, #Project ID or Usecase ID
    "transformerType": "Classification", #Options: Classification, Regression, Forcasting
    "training_dataset": "%s/model_assets/train.csv" % path, #path to csv file
    "test_dataset": "%s/model_assets/test.csv" % path, #path to csv file
    "pred_dataset": "%s/model_assets/pred.csv" % path, #path to csv file
    "actual_dataset": "%s/model_assets/truth.csv" % path, #path to csv file
    "model_file_path": "%s/model_assets/model.h5" % path, #path to model file
    "target_column": "label", #Target Column
    "note": "This is using Onprem.", #Short description of Model
    "model_area": "Area API test."
    }

ml_options = {
    "credPath": "/home/mizal/Projects/mmanager_test/scripts/config.json", #Path to Azure ML credential files.
    "datasetinsertionType": "Manual", #Option: AzureML, Manual
    "registryOption": ["Model","Dataset"], #To register model, add ["Model", "Dataset"] to register both model and datasets.
    "datasetUploadPath": "api_test_upload_jan17", #To registere dataset on path.
    }
Model(secret_key, url).post_model(model_data, ml_options)