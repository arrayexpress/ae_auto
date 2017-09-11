import json
import requests

from settings import CONAN_URL

__author__ = 'Ahmed G. Ali'


def get_rest_api_key(user_id):
    """
    Retrieves user rest Api Key by calling ``/api/users/USER_ID/restApiKey``

    :param user_id: User id in Conan database.
    :type user_id: int

    :return: rest API key for given user
    :rtype: str
    """
    url = CONAN_URL + 'api/users/%s/restApiKey' % user_id
    r = requests.get(url)
    return json.loads(r.text)['restApiKey']


def submit_task(pipeline_name, accession, rest_api_key, priority="MEDIUM", starting_index=0):
    """
    Submits a Conan task. Sending post request to ``api/submissions`` with data similar to the following JSON
    {
    "priority": `priority`,
    "pipelineName": `pipeline_name`,
    "startingProcessIndex": `starting_index`,
    "inputParameters": {"Accession Number": `accession`},
    "restApiKey": `rest_api_key`,
    }

    :param pipeline_name: Name of pipeline. e.g. load or unload ...etc.
    :type pipeline_name: str
    :param accession: ArrayExpress accession. e.g. E-MTAB-xxxx
    :type accession: str
    :param rest_api_key: User rest API key.
    :type rest_api_key: str
    :param priority: Task priority in the queue. default `MEDIUM`
    :type priority: str
    :param starting_index: The starting task number in the requested pipeline.
    :type starting_index: int
    :return: Submitted task ID.
    """
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
