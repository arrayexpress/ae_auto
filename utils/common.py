from subprocess import Popen, PIPE

__author__ = 'Ahmed G. Ali'


def execute_command(cmd, user=None):
    become_user = ''
    if user:
        become_user = ''

    p = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    return out, err