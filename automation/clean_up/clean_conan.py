from automation.release_date.geo import remove_geo_accession
from dal.oracle.ae2.plat_design import is_array_design_exists
from dal.oracle.conan.conan_tasks import update_task_status_by_id
from dal.oracle.conan.conan_transaction import retrieve_daemon_failed_tasks, \
    retrieve_daemon_more_than_week_running_tasks

__author__ = 'Ahmed G. Ali'


def main():
    tasks = retrieve_daemon_failed_tasks()
    for task in tasks:
        if 'A-GEOD' in task.name:
            if is_array_design_exists(task.name):
                print 'Array: %s found. Stopping task' % task.name
                before_after = 'before'
                if task.current_executed_index > 0:
                    before_after = 'after'
                update_task_status_by_id(id=task.id,status='ABORTED', status_message=task.status_message.replace('Failed at', 'Aborted '+before_after) )
        else:
            print 'Stopping task ' + task.name
            remove_geo_accession(task.name.replace('E-GEOD-', 'GSE'))
            before_after = 'before'
            if task.current_executed_index > 0:
                before_after = 'after'
            update_task_status_by_id(id=task.id,status='ABORTED', status_message=task.status_message.replace('Failed at', 'Aborted '+before_after) )
    # tasks = retrieve_daemon_more_than_week_running_tasks()
    # for task in tasks:
    #     print 'Stopping task ' + task.name
    #     remove_geo_accession(task.name.replace('E-GEOD-', 'GSE'))
    #     msg = task.status_message.replace('Doing', 'Aborted before')
    #     if task.current_executed_index == 0:
    #         msg = 'Aborted before the first process started'
    #     if task.current_executed_index > 0:
    #         msg = task.status_message.replace('Doing', 'Aborted after')
    #     update_task_status_by_id(id=task.id,status='ABORTED', status_message=msg)

if __name__ == '__main__':
    main()
