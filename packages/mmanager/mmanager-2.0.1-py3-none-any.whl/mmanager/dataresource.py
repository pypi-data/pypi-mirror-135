import json
import requests
import datetime


def get_model_data(model_data):
    registryOption = model_data.get('registryOption', None) 
    if registryOption:
        registryOption = json.dumps(registryOption)

    fetchOption = model_data.get('fetchOption', None)
    if fetchOption:
        fetchOption = json.dumps(fetchOption)

    data = {
            "project": model_data.get('project', None),
            "transformerType": model_data.get('transformerType', None),
            "algorithmType": model_data.get('algorithmType', None),
            "target_column": model_data.get('target_column', None),
            "modelFramework": model_data.get('modelFramework', None),
            "datasetinsertionType": model_data.get('datasetinsertionType', None),
            "note": model_data.get('note', None),
            "model_area": model_data.get('model_area', None),
            "model_dependencies": model_data.get('model_dependencies', None),
            "model_usage": model_data.get('model_usage', None),
            "model_adjustment": model_data.get('model_adjustment', None),
            "model_developer": model_data.get('model_developer', None),
            "model_approver": model_data.get('model_approver', None),
            "model_maintenance": model_data.get('model_maintenance', None),
            "documentation_code": model_data.get('documentation_code', None),
            "implementation_plateform": model_data.get('implementation_plateform', None),
            "production": model_data.get('production', None),
            "model_file_path" : model_data.get('model_file_path', None),
            "scoring_file_path" : model_data.get('scoring_file_path', None),
            "binarize_scoring_flag": model_data.get('binarize_scoring_flag', None),
            "modelName": model_data.get('modelName', None),
            "registryOption": registryOption,
            "fetchOption": fetchOption,
            "dataPath": model_data.get('dataPath', None)
    }
    return data

def get_files(model_data):
        training_dataset = model_data.get('training_dataset', None)
        pred_dataset = model_data.get('pred_dataset', None)
        actual_dataset = model_data.get('actual_dataset', None)
        test_dataset = model_data.get('test_dataset', None)
        model_image_path = model_data.get('model_image_path', None)
        model_summary_path = model_data.get('model_summary_path', None)
        model_file_path = model_data.get('model_file_path', None)

        if training_dataset:
            training_dataset = open(training_dataset, 'rb')
        if pred_dataset:
            pred_dataset = open(pred_dataset, 'rb')
        if actual_dataset:
            actual_dataset = open(actual_dataset, 'rb')
        if test_dataset:
            test_dataset = open(test_dataset, 'rb')
        if model_image_path:
            model_image_path = open(model_image_path, 'rb')
        if model_summary_path:
            model_summary_path = open(model_summary_path, 'rb')
        if model_file_path:
            model_file_path = open(model_file_path, 'rb')

        files = {
            "training_dataset": training_dataset,
            "test_dataset": test_dataset,
            "pred_dataset": pred_dataset,
            "actual_dataset": actual_dataset,
            "model_image_path": model_image_path,
            "model_summary_path": model_summary_path,
            "model_file_path": model_file_path
        }

        return files
