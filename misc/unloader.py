from utils.conan.conan import submit_conan_task

__author__ = 'Ahmed G. Ali'

experiments = """E-GEOD-19824
E-GEOD-32202
E-GEOD-38612
E-GEOD-48851
E-GEOD-49090
E-GEOD-49950
E-GEOD-51304
E-GEOD-58958
E-GEOD-58974
E-GEOD-59637
E-GEOD-61830
E-GEOD-63355
E-GEOD-63512""".split('\n')
for e in experiments:
    # conan = ConanPage(url=settings.CONAN_URL)
    # conan.login(login_email=settings.CONAN_LOGIN_EMAIL)
    print e
    # conan.unload_experiment(e.strip())
    submit_conan_task(accession=e.strip(), pipeline_name=CONAN_PIPELINES.unload)