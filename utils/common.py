from subprocess import Popen, PIPE

import pwd

import os
from nbstreamreader import NonBlockingStreamReader as NBSR

__author__ = 'Ahmed G. Ali'


def execute_command(cmd, user=None):
    if user:
        cmd = "sudo -H -u %s bash -c '%s'" % (user, cmd)

    p = Popen([cmd], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = p.communicate()
    return out, err


if __name__ == '__main__':
    out, err =  execute_command('ssh oy-ena-login-1 "cd /fire/staging/aexpress; ls E-MTAB-5481"', 'fg_cur',)
    for i in out.split('\n'):
        print i
    print '=' *50
    for i in err.split('\n'):
        print i
    print '=' *50
    # out, err =  execute_command('cd; pwd; ls -lah', 'gemmy',)
    # for i in out.split('\n'):
    #     print i