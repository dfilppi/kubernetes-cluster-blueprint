from cloudify.exceptions import NonRecoverableError
from cloudify import ctx
import subprocess

CMD_APP = 'DOCKER_OPTS="--bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}"'


def edit_docker_config(flannel):

    with open('/tmp/docker', 'w') as fd:
        with open('/etc/default/docker', 'r') as fdin:
            for line in fdin:
                fd.write(line)

    with open('/tmp/docker', 'a') as fd:
        fd.write('{0}\n'
                 '{1}\n'.format(flannel, CMD_APP)
                 )

    try:
        subprocess.call('sudo mv /tmp/docker /etc/default/docker', shell=True)
    except:
        raise NonRecoverableError('Unable to move Docker config into place.')


if __name__ == '__main__':

    ctx.logger.info('Configuring Flannel')

    flannel_args = ctx.instance.runtime_properties['flannel']

    edit_docker_config(flannel_args)
