import os
import stat
import urllib
from cloudify.exceptions import NonRecoverableError
from cloudify import ctx

URL = 'http://storage.googleapis.com/kubernetes-release/release/v1.0.1/bin/linux/amd64/kubectl'

PATH = os.path.join(
	os.path.expanduser('~'),
	'kubectl'
)


if __name__ == '__main__':

    ctx.logger.info('Installing kubectl')

    try:
        urllib.urlretrieve(URL, PATH)
    except:
    	raise NonRecoverableError()

    st = os.stat(PATH)
    os.chmod(PATH, st.st_mode | stat.S_IEXEC)
