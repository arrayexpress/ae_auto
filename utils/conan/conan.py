import settings
from dal.oracle.conan.conan_users import retrieve_user_by_email
from models.conan import CONAN_PIPELINES
from resources.conan import submit_task, get_rest_api_key

__author__ = 'Ahmed G. Ali'


def submit_conan_task(accession, pipeline_name, email=None, starting_index=0):
    """
    Submits a tast to Conan given login email and task name.

    :param accession: AE Accession. e.g. E-MTAB-xxxx
    :type accession: str
    :param pipeline_name: Conan pipeline name. e.g. ``AE2 Experiment Unloading``
    :type pipeline_name: str
    :param email: login email
    :type email: str
    :param starting_index: Starting process index in the pipeline.
    :type starting_index: int
    """
    if not email:
        email = settings.CONAN_LOGIN_EMAIL
    user = retrieve_user_by_email(email)[0]
    task_id = submit_task(pipeline_name=pipeline_name, accession=accession,
                          rest_api_key=get_rest_api_key(user.id),
                          priority="MEDIUM", starting_index=starting_index)
    print task_id


if __name__ == '__main__':
    submit_conan_task(accession='E-GEOD-37211', pipeline_name=CONAN_PIPELINES.unload)

