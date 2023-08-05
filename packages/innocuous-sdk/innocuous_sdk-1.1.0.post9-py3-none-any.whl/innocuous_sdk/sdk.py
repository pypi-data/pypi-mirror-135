import os
import yaml
from innocuous_api import InnocuousAPI

class InnocuousSDK:
    def __init__(self, token=None, **kwargs):
        self.version = "1.0.0"
        if token:
            self.token = token
        else:
            self.token = os.getenv("INNOCUOUSBOOK_TOKEN", "")

        self.api = InnocuousAPI(self.token, **kwargs)

    def get_experiment(self, id):
        return self.api.get_experiment(id)

    def get_endpoint(self, id):
        return self.api.get_endpoint(id)

    def list_experiments(self):
        return self.api.list_experiments()

    def list_endpoints(self):
        return self.api.list_endpoints()

    def get_experiment_id_by_name(self, name):
        result = [exp['id'] for exp in self.list_experiments() if exp["name"] == name]
        if len(result) < 2:
            return result[0]
        else:
            return result

    def get_endpoint_id_by_name(self, name):
        result = [endp['id'] for endp in self.list_endpoints() if endp["name"] == name]
        if len(result) < 2:
            return result[0]
        else:
            return result

    def create_experiment(self, recipe=None, yaml_path=None):
        """
        recipe - a python dict
        yaml_path - the path to a yaml file 
        ** Do not use both 
        """
        if yaml_path:
            with open(yaml_path, 'r') as f:
                recipe = yaml.safe_load(f)
        elif recipe is None:
            raise Exception('Either recipe or yaml_path argument need to exist to create an experiment')

        return self.api.create_experiment(recipe)

    def predict(self, id, data):
        return self.api.call_endpoint_predict(id, data)

    def predict_file(self, id, files):
        return self.api.call_endpoint_predict_file(id, files)

    def continuous_learning(self, id, dataset):
        return self.api.call_endpoint_continuous_learning(id, dataset)
