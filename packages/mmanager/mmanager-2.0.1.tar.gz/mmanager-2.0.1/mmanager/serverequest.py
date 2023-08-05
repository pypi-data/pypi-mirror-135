import os
import json
import requests


# def reg_no_ml_options(data):
#     credPath = input("Enter registered credential file path: ")
#     if os.path.exists(credPath):
#         f = open(credPath)
#         creds = json.load(f)
#         print(creds)
#     else:
#         print("Credential file path invalid.")
#         exit()
        
#     registerOption = input("Enter 0 to register model and upload datasets to Azure ML workspace.\nEnter 1 to register model to Azure ML.\nEnter 2 to upload datasets to Azure ML workspace. : ")
#     if int(registerOption) == 0 or int(registerOption) == 2:
#         datasetUploadPath = input("Enter dataset upload path: ")
#     else:
#         datasetUploadPath = None
#     data.update({"credId": json.dumps(creds), "registerOption": int(registerOption), "datasetUploadPath": datasetUploadPath})       
#     return data

# def fetch_no_ml_options(data):
#     credPath = input("Enter registered credential file path: ")
#     if os.path.exists(credPath):
#         f = open(credPath)
#         creds = json.load(f)
#         print(creds)
#     else:
#         print("Credential file path invalid.")
#         exit()
    
#     fetch_list = []
#     fetchOption = input("Enter 0 to fetch model and upload datasets from Azure ML workspace.\nEnter 1 to fetch model from Azure ML.\nEnter 2 to fetch datasets from Azure ML workspace. : ")

#     if fetchOption == 0:
#         fetch_list.append(["Model", "Datasets"])
#     elif fetchOption == 1:
#         fetch_list.append(["Model"])
#     else:
#         fetch_list.append(["Datasets"])

#     if int(fetchOption) == 0 or int(fetchOption) == 2:
#         dataPath = input("Enter dataset path: ")
#     else:
#         dataPath = None
#     data.update({"credId": json.dumps(creds), "fetchOption": fetch_list, "dataPath": dataPath})       
#     return data

def reg_ml(data, ml_options):
    datasetUploadPath = ml_options["datasetUploadPath"]
    if os.path.exists(ml_options["credPath"]):
                f = open(ml_options["credPath"])
                creds = json.load(f)
                print(creds)
    else:
        print("Credential file path invalid.")
        exit()
    data.update({"amlCred": json.dumps(creds), "datasetUploadPath": datasetUploadPath})
    return data

def fetch_ml(data, ml_options):
    dataPath = ml_options["dataPath"]
    if os.path.exists(ml_options["credPath"]):
                f = open(ml_options["credPath"])
                creds = json.load(f)
                print(creds)
    else:
        print("Credential file path invalid.")
        exit()
    data.update({"amlCred": json.dumps(creds), "dataPath": dataPath})
    return data

def model_request(url, kwargs, data, ml_options, files):
    insertionType = data.get("datasetinsertionType", None)
    if insertionType == "Manual":
        data = reg_ml(data, ml_options)
        model = requests.post(url, data=data, files=files, headers=kwargs['headers'])
    elif insertionType == "AzureML":
        data = fetch_ml(data, ml_options)
        data.update(files)
        model = requests.post(url, data=data, headers=kwargs['headers'])
    else:
        model = requests.post(url, data=data, files=files, headers=kwargs['headers'])
    return model
    