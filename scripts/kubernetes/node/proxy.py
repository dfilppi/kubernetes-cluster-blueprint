from cloudify import ctx
import subprocess
from cloudify.state import ctx_parameters as inputs


def run_proxy(ip, port):

    subprocess.call(
        'sudo docker run -d --net=host --privileged '
        'gcr.io/google_containers/hyperkube:v1.0.1 '
        '/hyperkube proxy '
        '--master=http://{0}:{1} --v=2'
        .format(ip, port),
        shell=True
    )


if __name__ == '__main__':

    ctx.logger.info('Initializing Proxy')

    master_ip = inputs['master_ip']
    ctx.logger.info('Master IP: {0}'.format(master_ip))

    master_port = inputs['master_port']
    ctx.logger.info('Master Port: {0}'.format(master_port))

    run_proxy(master_ip, master_port)
