import json
import requests

from settings import CONAN_URL

__author__ = 'Ahmed G. Ali'


def get_rest_api_key(user_id):
    # http://banana.ebi.ac.uk:14054/conan2/api/users/840508/restApiKey
    url = CONAN_URL + 'api/users/%s/restApiKey' % user_id
    r = requests.get(url)
    return json.loads(r.text)['restApiKey']


def submit_task(pipeline_name, accession, rest_api_key, priority="MEDIUM", starting_index=0):
    url = CONAN_URL + 'api/submissions'
    data = {
        "priority": priority,
        "pipelineName": pipeline_name,
        "startingProcessIndex": str(starting_index),
        "inputParameters": {"Accession Number": accession},
        "restApiKey": str(rest_api_key),
    }
    r = requests.post(url=url, json=data)
    print r.text
    return json.loads(r.text)['submittedTaskID']

if __name__ == '__main__':
    print submit_task("MAGE-TAB Export", "E-ERAD-428", get_rest_api_key(840508))
