import json
import os
from braces.views import JSONResponseMixin
from django.http import HttpResponse

from django.views.generic.base import View
from pinax.eventlog.models import log
from accounts.models import User
from maintenance.models import Validate, STATUS
from utils.common import execute_command
from utils.email.sender import send_email
from utils.maintenance import spring_framework
from django.views.decorators.csrf import csrf_exempt


class RestartFramework(JSONResponseMixin, View):
    def post(self, request):
        out = spring_framework.main()
        log(
            user=request.user,
            action='Restart Framework',
            extra={'out': out}

        )
        print request.user
        print dir(request.user)
        print 'USERNAME: ', request.user.username

        user = User.objects.get(username=request.user.username)
        print user
        body = """Hi %s,
The framework is restarted according to your request.
Kindly wait couple of mins and then restart/start your Conan Processes.

Have a nice day!
AE Automation Tool.""" % user.first_name
        send_email(from_email='AE Automation<ae-automation@ebi.ac.uk>', to_emails=[request.user.email],
                   subject='Framework Restarted', body=body)
        return self.render_json_response({}, 200)


@csrf_exempt
def validate_data_files_view(request, job_id=''):
    if request.method == "POST":
        req_id = request.POST.get('id')
        data_dir = request.POST.get('data_dir')
        v = Validate.objects.filter(job_id=req_id)
        report = {'file_errors': {}, 'pairs_errors': [], 'valid_files': [], 'execution_errors': [], 'integrity_errors': []}
        if v:
            v = v[0]
            v.data_dir = data_dir
            v.validation_report = json.dumps(report)
            v.status = 'P'
        else:
            v = Validate(job_id=str(req_id), data_dir=data_dir, validation_report=json.dumps(report))
        v.save()
        py_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'utils', 'validators', 'fastq_validators.py'))
        cmd = """ssh ebi-login-001 "source /etc/profile.d/lsf.sh;bsub -u ahmed -q production-rh7 'source /nfs/production3/ma/home/arrayexpress/ae_automation/resources-rh7/bashrc;which python; python %s %s %s'" """ % (py_file, req_id, data_dir)
        # cmd = """export PYTHONPATH="${PYTHONPATH}:/home/gemmy/PycharmProjects/ae_automation";source /home/gemmy/automation/bin/activate; python %s %s %s """ % (
        #     py_file, req_id, data_dir)
        print cmd
        out, err = execute_command(cmd)
        print out
        print '=' * 30
        print err
        return HttpResponse({}, 200)

    if request.method == "GET":
        # job_id = getattr(request, 'job_id')
        if not job_id:
            return HttpResponse('Bad Request', 400)
        v = Validate.objects.filter(job_id=job_id)
        if not v:
            return HttpResponse('Not Fount', 404)
        report = json.loads(v[0].validation_report)
        report['status'] = [i[1] for i in STATUS if i[0] == v[0].status][0]
        del report['execution_errors']
        return HttpResponse(json.dumps(report), 200)
