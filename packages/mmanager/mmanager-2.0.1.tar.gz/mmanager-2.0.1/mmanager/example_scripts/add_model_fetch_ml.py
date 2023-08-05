from mmanager.mmanager import Model
secret_key = '9cb2825b932f33e40556de3dfd415c0f395503e5'
url = 'http://localhost:8000'
model_data = {
    "project": 46, #Project ID or Usecase ID
    "transformerType": "Classification", #Options: Classification, Regression, Forcasting
    "training_dataset": "",
    "test_dataset": "",
    "pred_dataset": "",
    "actual_dataset": "",
    "model_file_path": "", 
    "target_column": "label", #Target Column
    "note": "" #Short description of Model
    }

ml_options = {
    "credPath": "config.json", #Path to Azure ML credential files.
    "datasetinsertionType": "AzureML", #Option: AzureML, Manual
    "fetchOption": ["Model"], #To fetch model, add ["Model", "Dataset"] to fetch both model and datasets.
    "modelName": "histo", #Fetch model file registered with model name.
    "dataPath": "dataset-name", #Get datasets registered with dataset name.
    }
Model(secret_key, url).post_model(model_data, ml_options)