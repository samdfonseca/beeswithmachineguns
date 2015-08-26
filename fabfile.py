import os
from merge_reports import merge_results
import boto.ec2
from beeswithmachineguns.bees import _read_server_list, _get_region, _get_pem_path
from fabric.api import run, env, get

def set_hosts():
    username, key_name, zone, instance_ids = _read_server_list()
    ec2_connection = boto.ec2.connect_to_region(_get_region(zone))
    existing_reservations = ec2_connection.get_all_instances(instance_ids=instance_ids)
    existing_instances = []
    map(existing_instances.extend, [r.instances for r in existing_reservations])
    env.hosts = [instance.ip_address for instance in existing_instances]
    env.user = username
    env.key_filename = _get_pem_path(key_name)

def runinit():
    run('/tmp/init.sh')

def runbench():
    run('cd /tmp && make bench')
    file = '/tmp/simple-bench.xml'
    get(file, env.host_string+'-simple-bench.xml')
    merge_results()
    os.system('fl-build-report --html results.xml')
