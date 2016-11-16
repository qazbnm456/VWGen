import platform
import os
import re
import time
import json
from docker import Client
from docker.errors import APIError, NullResource, NotFound
from .logger import Logger

try:
    import urlparse
except ImportError:  # For Python 3
    import urllib.parse as urlparse

nonspace = re.compile(r'\S')


def jsoniterparse(j):
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded


class time_limit(object):

    def __init__(self, seconds):
        self.seconds = seconds

    def __enter__(self):
        self.die_after = time.time() + self.seconds
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def timed_reset(self):
        self.die_after = time.time() + self.seconds

    @property
    def timed_out(self):
        return time.time() > self.die_after


class dockerAgent(object):
    """Class for manipulating the docker client."""

    host = None
    client = None
    ctr = None
    current_ctr = None

    def __init__(self):
        """Loading docker environments"""
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            try:
                # TLS problem, can be referenced from
                # https://github.com/docker/machine/issues/1335
                from docker.utils import kwargs_from_env
                self.host = '{0}'.format(urlparse.urlparse(
                    os.environ['DOCKER_HOST']).netloc.split(':')[0])
                self.client = Client(
                    base_url='{0}'.format(os.environ['DOCKER_HOST']))
                kwargs = kwargs_from_env()
                kwargs['tls'].assert_hostname = False
                self.client = Client(**kwargs)
            except KeyError:
                self.host = '127.0.0.1'
                self.client = Client(base_url='unix://var/run/docker.sock')
        else:
            self.host = '127.0.0.1'
            self.client = Client(base_url='unix://var/run/docker.sock')

    def createHostConfig(self, port_bindings, binds, links):
        """Create host config for containers"""
        return self.client.create_host_config(port_bindings=port_bindings, binds=binds, links=links)

    def startContainer(self, image, name, ports=None, volumes=None, environment=None, host_config=None, tty=False, command=None):
        """Start containers"""
        try:
            self.ctr = self.client.create_container(
                image=image, name=name, ports=ports, volumes=volumes, environment=environment, host_config=host_config, tty=tty, command=command)
        except (TypeError, APIError), e:
            Logger.logError("\n" + "[ERROR] " + str(e.explanation))
            for line in self.client.pull(image, stream=True):
                for iterElement in list(jsoniterparse(line)):
                    Logger.logInfo(
                        "[INFO] " + json.dumps(iterElement, indent=4))
            self.ctr = self.client.create_container(
                image=image, name=name, ports=ports, volumes=volumes, environment=environment, host_config=host_config, tty=tty, command=command)
        except NullResource:
            pass
        self.current_ctr = self.ctr
        self.client.start(self.ctr)
        return self.ctr

    def removeContainer(self, ctr):
        """Remove containers"""
        try:
            if ctr is not None:
                self.client.remove_container(
                    ctr, force=True)
            else:
                self.client.remove_container(
                    self.current_ctr, force=True)
        except (NotFound, NullResource):
            pass
        except (TypeError, APIError), e:
            Logger.logError("\n" + "[ERROR] " + str(e.explanation))

    def execute(self, ctr, cmd, path):
        """Execute commands for giving ctr"""
        try:
            with time_limit(600) as t:
                for line in self.client.exec_start(self.client.exec_create(ctr, "/bin/bash -c 'cd {0} && {1}'".format(path, cmd)), stream=True):
                    time.sleep(0.1)
                    Logger.logInfo("[INFO] " + line)
                    if t.timed_out:
                        break
                    else:
                        t.timed_reset
        except (NotFound, NullResource):
            pass
        except (TypeError, APIError), e:
            Logger.logError("\n" + "[ERROR] " + str(e.explanation))

    def logs(self, ctr):
        """Logging collection from docker daemon"""
        try:
            with time_limit(600) as t:
                for line in self.client.logs(ctr, stderr=False, stream=True):
                    time.sleep(0.1)
                    Logger.logInfo("[INFO] " + line)
                    if t.timed_out:
                        break
                    else:
                        t.timed_reset
        except (NotFound, NullResource):
            pass
        except (TypeError, APIError), e:
            Logger.logError("\n" + "[ERROR] " + str(e.explanation))
