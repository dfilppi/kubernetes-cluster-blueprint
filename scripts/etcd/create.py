from cloudify import ctx
import os
import time
from cloudify.state import ctx_parameters as inputs


def start_etcd(etcd_version):

    res = os.system(
        'sudo docker -H unix:///var/run/docker-bootstrap.sock '
        'run --net=host -d gcr.io/google_containers/etcd:{0} '
        '/usr/local/bin/etcd --addr=127.0.0.1:4001 '
        '--bind-addr=0.0.0.0:4001 --data-dir=/var/etcd/data'.format(etcd_version)
    )

    ctx.logger.info("start etcd:"+str(res))

    if res:
        return res

    time.sleep(2)


def setup_cidr_range_for_flannel(etcd_version):

    os.system(
        'sudo docker -H unix:///var/run/docker-bootstrap.sock '
        'run --net=host gcr.io/google_containers/etcd:{0} '
        'etcdctl set /coreos.com/network/config '
        '\'{{ "Network": "10.1.0.0/16" }}\''.format(etcd_version)
    )


if __name__ == '__main__':

    ctx.logger.info('Initializing ETCD')

    version = inputs['etcd_version']

    start_etcd(version)

    setup_cidr_range_for_flannel(version)
