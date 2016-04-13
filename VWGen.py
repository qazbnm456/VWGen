import platform
import os
import sys
import optparse
import zipfile
import shutil
import web
from web import form
import time

from docker import Client
if platform.system() == 'Darwin' or platform.system() == 'Windows':
    from docker.utils import kwargs_from_env  # TLS problem, can be referenced from https://github.com/docker/machine/issues/1335
    web.host = '192.168.99.100'
    client = Client(base_url='tcp://{0}:2376'.format(web.host))
    kwargs = kwargs_from_env()
    kwargs['tls'].assert_hostname = False
    client = Client(**kwargs)
else:
    web.host = '127.0.0.1'
    client = Client(base_url='unix://var/run/docker.sock')

parent_dir = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
if os.path.exists(os.path.join(parent_dir, "demo")):
    sys.path.append(parent_dir)
from demo.demo import Demo
THEME_DIR = os.path.dirname(sys.modules['demo'].__file__)

demo = Demo()  # testing for now
out = ''
ctr = None

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


class VWGen(object):
    def __init__(self, theme):
        self.theme_name = "startbootstrap-clean-blog-1.0.3"  # testing for now
        self.theme_path = os.path.join(THEME_DIR, "themes", self.theme_name)
        self.output = os.path.join(THEME_DIR, "output")
        self.backend = ""
        self.image = ""
        self.dbms = ""
        self.attacks = []
        self.options = None
        self.source = None

    def __initBackend(self):
        # Do Backend Environment Initialization
        self = self

    def _index__initThemeEnv(self):
        self.__initBackend()
        with zipfile.ZipFile(self.theme_path + '.zip', "r") as z:
            z.extractall(self.output)
        with open(os.path.join(self.output, self.theme_name, "index.html"), 'rb') as src:
            self.source = src.read()

    def __initAttacks(self):
        from core.attack import attack

        print("[*] Loading modules:")
        print(u"\t {0}".format(u", ".join(attack.modules)))

        for mod_name in attack.modules:
            mod = __import__("core.attack." + mod_name, fromlist=attack.modules)
            mod_instance = getattr(mod, mod_name)()

            self.attacks.append(mod_instance)
            self.attacks.sort(lambda a, b: a.PRIORITY - b.PRIORITY)

    def generate(self):
        self.__initAttacks()
        for x in self.attacks:
            print('')
            if x.require:
                t = [y.name for y in self.attacks if y.name in x.require]
                if x.require != t:
                    print("[!] Missing dependencies for module {0}:".format(x.name))
                    print(u"  {0}".format(",".join([y for y in x.require if y not in t])))
                    continue
                else:
                    x.loadRequire([y for y in self.attacks if y.name in x.require])

            x.logG(u"[+] Launching module {0} and its deps: {1}".format(x.name, ",".join([y.name for y in self.attacks if y.name in x.require])))
            
            target_dir = os.path.join(self.output, self.theme_name)
            web.payloads = x.Job(self.source, self.backend, self.dbms, target_dir)

            return [self.output, os.path.join(self.output, self.theme_name)]

    def setBackend(self, backend="php"):
        self.backend = backend
        if self.backend == 'php':
            self.image = 'richarvey/nginx-php-fpm'
            self.mount_point = '/usr/share/nginx/html'

    def setDBMS(self, DBMS):
        self.dbms = DBMS
        web.container_name = '{0}_ctr'.format(self.dbms)
        if self.dbms is not None:
            if self.dbms == 'Mysql':
                web.db_ctr = web.client.create_container(image='mysql', name='{0}'.format(web.container_name),
                    environment={
                        "MYSQL_ROOT_PASSWORD": "root_password",
                        "MYSQL_DATABASE": "root_mysql"
                    }
                )
                web.client.start(web.db_ctr)
            elif self.dbms == 'Mongo':
                web.db_ctr = web.client.create_container(image='mongo', name='{0}'.format(web.container_name))
                web.client.start(web.db_ctr)


    def setModules(self, options=""):
        self.options = options


urls = (
    '/', 'index',
)


index_render = web.template.render('templates/')
cubic_render = web.template.render('demo/cubic/')
app = web.application(urls, globals())

myform = form.Form(
    form.Hidden(id='HH', name='hash', value='')
)


class index:
    def GET(self):
        form = myform()
        return index_render.index(form)

    def POST(self):
        web.header('Content-type', 'text/html')
        web.header('Transfer-Encoding', 'chunked')
        form = myform()
        if not form.validates():
            yield index_render.formtest(form)
        else:
            info = form['hash'].value.split('_')
            try:
                global client, ctr
                web.client = client
                web.ctr = ctr
                gen = VWGen(int(info[2]))
                gen.setBackend()
                gen.setDBMS(web.dbms)
                gen._index__initThemeEnv()
                [folder, path] = gen.generate()
                web.path = path
                web.ctr = web.client.create_container(image='{0}'.format(gen.image), ports=[80], volumes=['{0}'.format(gen.mount_point)],
                    host_config=web.client.create_host_config(
                        port_bindings={
                            80: web.expose
                        },
                        binds={
                            "{0}".format(path): {
                                'bind': '{0}'.format(gen.mount_point),
                                'mode': 'rw',
                            }
                        },
                        links={ '{0}'.format(web.container_name): '{0}'.format(gen.dbms) } if gen.dbms is not None else None
                    )
                , name='VW')
                web.client.start(web.ctr)

                try:
                    import urlparse
                    from urllib import urlencode
                except: # For Python 3
                    import urllib.parse as urlparse
                    from urllib.parse import urlencode
                url = ['http', '{0}:{1}'.format(web.host, web.expose), '/', '', '', '']
                params = {}

                for index, _ in enumerate(web.payloads['key']):
                    params.update({'{0}'.format(web.payloads['key'][index]): '{0}'.format(web.payloads['value'][index])})

                query = params

                url[4] = urlencode(query)

                print "Browse: {0}".format(urlparse.urlunparse(url))

                global out
                with time_limit(5) as t:
                    yield '<tt>'
                    for line in web.client.logs(web.ctr, stderr=False, stream=True):
                        # out += line
                        # print line
                        line = line.replace(" ", "&nbsp;")
                        time.sleep(0.1)
                        yield line + '</br>'
                        if t.timed_out or "END" in line:
                            break
                        else:
                            t.timed_reset
                    yield '</tt>'
            except SystemExit:
                pass


if __name__ == "__main__":
    try:
        usage = "usage: %prog [options] arg1 arg2"
        p = optparse.OptionParser(usage=usage)
        p.add_option('--port', '-p',
                    action="store", dest="port", type="int", default=8080, metavar='PORT',
                    help="Configure the port this server to listen on")
        p.add_option('--expose',
                    action="store", dest="expose", type="int", default=80, metavar='PORT',
                    help="Configure the port of the host for container binding")
        p.add_option('--database',
                    action="store", dest="dbms", type="string", default=None, metavar='DBMS',
                    help="Configure the dbms for container linking")
        p.add_option('--module', '-m',
                    action="store", dest="modules", default=None, metavar='MODULES_LIST',
                    help="List of modules to load")
        p.add_option('--verbose', '-v',
                    action="store", dest="verbosity", type="int", default=0, metavar='LEVEL',
                    help="Set verbosity level")
        p.add_option('--file',
                    action="store", dest="source", type="string", default=None, metavar='FILENAME',
                    help="[Not supported yet] Specify the file that VWGen will gonna operate on")
        options, arguments = p.parse_args()

        # set sys.argv to the remaining arguments after
        # everything consumed by optparse
        if options.source is not None:
            web.source = options.source

            # This is not required if you've installed pycparser into
            # your site-packages/ with setup.py
            #
            sys.path.extend(['./core/pycparser'])
            from pycparser import parse_file

            ast = parse_file(web.source, use_cpp=True,
                    cpp_path='gcc',
                    cpp_args=['-E', r'-Iutils/fake_libc_include'])

            ast.show()

        web.expose = options.expose
        web.dbms = options.dbms
        web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", options.port))
    finally:
        from docker.errors import APIError
        print "\nClose..."
        try:
            shutil.rmtree(web.path)
            try:
                web.client.stop(web.db_ctr) if web.db_ctr is not None else None
                web.client.stop(web.ctr)
            except APIError:
                web.client.wait(web.db_ctr) if web.db_ctr is not None else None
                web.client.wait(web.ctr)
            try:
                web.client.remove_container(web.db_ctr, force=True) if web.db_ctr is not None else None
                web.client.remove_container(web.ctr, force=True)
            except APIError:
                pass
        except AttributeError:
            pass
