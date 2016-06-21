import subprocess
from cloudify.state import ctx_parameters as inputs


def run_proxy(port):

    subprocess.call(
        'sudo docker run -d --net=host --privileged '
        'gcr.io/google_containers/hyperkube:v1.0.1 '
        '/hyperkube proxy --master=http://127.0.0.1:{0} '
        '--v=2'.format(port),
        shell=True
    )


if __name__ == '__main__':

    master_port = inputs['master_port']
    run_proxy(master_port)
