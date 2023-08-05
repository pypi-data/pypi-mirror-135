# Welcome to Modelmanager-api!

## This is a api model for interacting with modelmanager.

> **Note:**
>
> - Example files are are in example_script directory.
> - Example assets are in assets directory.
> - It contains scripts for different actions(Add, Update, Delete).

---

## **Example Codes**

## Add Project / Usecase

```python
from mmanager.mmanager import Usecase
secret_key = 'Secret-Key'
url = 'URL'
data = {
		"name": "UsecaseName",
		"author": "AuthorName",
		"description": "UsecaseDescription",
		"source": "UsecasSource",
		"contributor": "UsecaseContributor",
		"image": 'image.jpg' , #path to image file
		"banner": 'banner.jpg' , #path to banner file
	}
Usecase(secret_key, url).post_usecase(data)
```

---

## Update Project

```python
from mmanager.mmanager import Usecase
secret_key = 'Secret-Key'
url = 'URL'
project_id = Project_id #use model_id number to update
data = {
		"author": "AuthorName",
		"description": "UsecaseDescription",
		"source": "UsecasSource",
		"contributor": "UsecaseContributor",
		"image": 'image.jpg' , #path to image file
		"banner": 'banner.jpg' , #path to banner file
	}
Usecase(secret_key, url).patch_usecase(data, project_id)
```

---

## Delete Project

```python
from mmanager.mmanager import Usecase
secret_key = 'Secret-Key'
url = 'URL'
project_id = Project_id #use project_id number to delete
Usecase(secret_key,url).delete_usecase(project_id)
```

---


## Create Config File For Azure ML Credentials
- Get Credentials from your existing Azure ML account.
- Create a config file in following format 
- Give credential file path in credPath field to enable using AML integration service.

```json
{
    "subscription_id": "<subscription-id>",
    "resource_group": "<resource_group>",
    "workspace_name": "<workspace_name>",
    "tenant-id": "<tenant-id>",
    "datastore_name": "<datastore_name>"
}
```

---

## Add Model No ML Integration

```python
from mmanager.mmanager import Model
secret_key = 'Secret-Key'
url = 'URL'
path = 'assets' #path to csv file

model_data = {
    "project": "<project-id>", #Project ID or Usecase ID
    "transformerType": "model-type", #Options: Classification, Regression, Forcasting
    "training_dataset": "%s/model_assets/train.csv" % path, #path to csv file
    "test_dataset": "%s/model_assets/test.csv" % path, #path to csv file
    "pred_dataset": "%s/model_assets/pred.csv" % path, #path to csv file
    "actual_dataset": "%s/model_assets/truth.csv" % path, #path to csv file
    "model_file_path": "%s/model_assets/model.h5" % path, #path to model file
    "target_column": "target-column-name", #Target Column
    "note": "" #Short description of Model
}
Model(secret_key, url).post_model(model_data)
```
## Additional model fields
```json
{
    "model_area": "",
    "model_dependencies": "",
    "model_usage": "",
    "model_audjustment": "",
    "model_developer": "",
    "model_approver": "",
    "model_maintenance": "",
}
```
## Add Model, Fetch Datasets And Model From Azure ML

```python
from mmanager.mmanager import Model
secret_key = 'Secret-Key'
url = 'URL'
model_data = {
    "project": "<project-id>", #Project ID or Usecase ID
    "transformerType": "model-type", #Options: Classification, Regression, Forcasting
    "training_dataset": "",
    "test_dataset": "",
    "pred_dataset": "",
    "actual_dataset": "", 
    "model_file_path": "", 
    "target_column": "target-column-name", #Target Column
    "note": "" #Short description of Model
    }

ml_options = {
    "credPath": "config.json", #Path to Azure ML credential files.
    "datasetinsertionType": "AzureML", #Option: AzureML, Manual
    "fetchOption": ["Model"], #To fetch model, add ["Model", "Dataset"] to fetch both model and datasets.
    "modelName": "model-name", #Fetch model file registered with model name.
    "dataPath": "dataset-name", #Get datasets registered with dataset name.
    }
Model(secret_key, url).post_model(model_data, ml_options)
```
## Add Model, Upload Datasets And Model Manually And Register To Azure ML

```python
from mmanager.mmanager import Model
secret_key = 'Secret-Key'
url = 'URL'
path = 'assets' #path to csv file
model_data = {
    "project": "<project-id>", #Project ID or Usecase ID
    "transformerType": "model-type", #Options: Classification, Regression, Forcasting
    "training_dataset": "%s/model_assets/train.csv" % path, #path to csv file
    "test_dataset": "%s/model_assets/test.csv" % path, #path to csv file
    "pred_dataset": "%s/model_assets/pred.csv" % path, #path to csv file
    "actual_dataset": "%s/model_assets/truth.csv" % path, #path to csv file
    "model_file_path": "%s/model_assets/model.h5" % path, #path to model file
    "target_column": "target-column-name", #Target Column
    "note": "", #Short description of Model
    "model_area": "Area API test."
    }

ml_options = {
    "credPath": "config.json", #Path to Azure ML credential files.
    "datasetinsertionType": "Manual", #Option: AzureML, Manual
    "registryOption": ["Model"], #To register model, add ["Model", "Dataset"] to register both model and datasets.
    "datasetUploadPath": "dataset-name", #To registere dataset on path.
    }
Model(secret_key, url).post_model(model_data, ml_options)
```
---

## Update Model

```python
from mmanager.mmanager import Model
secret_key = 'Secret-Key'
url = 'URL'
model_id = Model_id #use model_id number to update
data = {
		"transformerType": "logistic",
		"target_column": "id",
		"note": "api script Model",
		"model_area": "api script Model",
		"model_dependencies": "api script Model",
		"model_usage": "api script Model",
		"model_audjustment": "api script Model",
		"model_developer": "api script Model",
		"model_approver": "api script Model",
		"model_maintenance": "api script Model",
		"documentation_code": "api script Model",
		"implementation_plateform": "api script Model",
		"training_dataset": "train.csv", #path to csv file
		"pred_dataset": "submissionsample.csv", #path to csv file
		"actual_dataset": "truth.csv", #path to csv file
		"test_dataset": "test.csv", #path to csv file
		"model_file_path":"",
	    "scoring_file_path":"",
		"model_image_path":"" ,
    	"model_summary_path":"",
	}
Model(secret_key, url).patch_model(data, model_id)
```

---

# Delete Model

---

```python
from mmanager.mmanager import Model
secret_key = 'Secret-Key'
url = 'URL'
model_id = Model_id #use model_id number to delete
Model(secret_key,url).delete_model(model_id)
```

---
