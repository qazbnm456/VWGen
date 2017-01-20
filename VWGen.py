#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import optparse
import imp
import web
from blessed import Terminal
from docker.errors import APIError
from tsaotun.cli import Tsaotun
from core.file.filePointer import filePointer
from core.file.logger import Logger
from core.shell.shellAgent import shellAgent

try:
    import urlparse
    from urllib import urlencode
except ImportError:  # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

web.container_name = None
web.ctr = None
web.db_ctr = None
web.payloads = None
web.path = None
web.dAgent = Tsaotun()
web.fp = filePointer()


class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


def enter_shell(gen_instance):
    sA = shellAgent()
    gen_instance.parse("set backend = php")
    gen_instance.parse("set dbms    = None")
    gen_instance.parse("set theme   = startbootstrap-agency-1.0.6")
    gen_instance.parse("set expose  = 80")
    gen_instance.parse("set modules = +unfilter")
    Logger.logInfo("VWGen ready (press Ctrl+D to end input)")
    while True:
        result = gen_instance.parse(sA.prompt())
        if result == "CTRL+D":
            Logger.logInfo("[INFO] CTRL+D captured. Exit.")
            raise RuntimeError
        elif result is not None:
            Logger.logSuccess(result)
        else:
            Logger.logError("Unreconized keyword!")


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
from demo.demo import Demo
THEME_DIR = os.path.join(ROOT_DIR, 'demo')

demo = Demo()  # testing for now


class VWGen(object):

    def __init__(self):
        self.color = 0
        self.verbose = 0
        self.theme = None
        self.theme_path = None
        self.output = os.path.join(THEME_DIR, "output")
        self.backend = None
        self.image = None
        self.dbms = None
        self.expose = None
        self.attacks = []
        self.modules = None
        self.source = None
        self.fp = web.fp

        self.tty = False
        self.command = None

    def __initBackend(self):
        # Do Backend Environment Initialization
        pass

    def __initThemeEnv(self):
        self.__initBackend()
        self.fp.zipExtract(self.theme_path, self.output)
        self.source = self.fp.read(os.path.join(
            self.output, self.theme, self.fp.findMainPointer()))

    def __initAttacks(self):
        from core.attack import attack

        Logger.logInfo("[INFO] Loading modules:")
        Logger.logInfo(
            u"[INFO] " + "\t {0}".format(u", ".join(attack.modules)))

        for mod_name in attack.modules:
            f, filename, description = imp.find_module(
                mod_name, [os.path.join(ROOT_DIR, 'core', 'attack')])
            mod = imp.load_module(
                mod_name, f, filename, description)
            mod_instance = getattr(mod, mod_name)(self.fp)

            self.attacks.append(mod_instance)
            self.attacks.sort(lambda a, b: a.PRIORITY - b.PRIORITY)

        # Custom list of modules was specified
        if self.modules is not None:
            # First deactivate all modules
            for attack_module in self.attacks:
                attack_module.doReturn = False

            opts = self.modules.split(",")

            for opt in opts:
                if opt.strip() == "":
                    continue

                module = opt

                # deactivate some modules
                if module.startswith("-"):
                    module = module[1:]
                    if module == "all":
                        for attack_module in self.attacks:
                            if attack_module.name in attack.modules:
                                attack_module.doReturn = False
                    else:
                        found = False
                        for attack_module in self.attacks:
                            if attack_module.name == module:
                                found = True
                                attack_module.doReturn = False
                        if not found:
                            Logger.logError(
                                "[ERROR] Unable to find a module named {0}".format(module))

                # activate some modules
                else:
                    if module.startswith("+"):
                        module = module[1:]
                    else:
                        module = attack.default
                    if module == "all":
                        Logger.logError(
                            "[ERROR] Keyword 'all' was not safe enough for activating all modules at once. Specify modules names instead.")
                    else:
                        found = False
                        for attack_module in self.attacks:
                            if attack_module.name == module:
                                found = True
                                attack_module.doReturn = True
                        if not found:
                            Logger.logError(
                                "[ERROR] Unable to find a module named {0}".format(module))

    def reset(self):
        self.attacks = []
        self.source = None

    def setColor(self, default=1):
        self.color = default
        return self.color

    def setVerbose(self, default=1):
        self.verbose = default
        return self.verbose

    def generate(self):
        self.__initAttacks()

        deps = None
        for _, x in enumerate(self.attacks):
            if x.doReturn:
                print('')
                if x.require:
                    x.loadRequire(self.source, self.backend, self.dbms, [
                                  y for y in self.attacks if y.name in x.require])
                    deps = ", ".join(
                        [y.name for y in self.attacks if y.name in x.require])

        for x in self.attacks:
            if x.doReturn:
                Logger.logSuccess(u"[+] Launching module {0}".format(x.name))
                Logger.logSuccess(u"   and its deps: {0}".format(
                    deps if deps is not None else 'None'))
                if self.color:
                    x.setColor()
                if self.verbose:
                    x.setVerbose()
                web.payloads = x.Job(
                    self.source, self.backend, self.dbms)

        return os.path.join(self.output, self.theme)

    def setThemeEnv(self):
        self.__initThemeEnv()

    def setBackend(self, backend="php"):
        if backend == "None":
            backend = None
        self.backend = backend
        for case in switch(self.backend):
            if case('php'):
                self.image = 'richarvey/nginx-php-fpm:php5'
                self.mount_point = '/var/www/html'
                return self.backend
            if case('php7'):
                self.image = 'richarvey/nginx-php-fpm:php7'
                self.mount_point = '/var/www/html'
                return self.backend
            if case('node'):
                self.tty = True
                self.image = 'node:latest'
                self.mount_point = '/usr/src/app'
                return self.backend
            if case():
                Logger.logError("[ERROR] Not supported backend!")
                self.backend = "php"
                Logger.logInfo(
                    "[Info] set backend to {0}!".format(self.backend))
                return self.backend

    def setDbms(self, Dbms=None):
        if Dbms == "None":
            Dbms = None
        self.dbms = Dbms
        web.container_name = '{0}_ctr'.format(self.dbms)
        if self.dbms is not None:
            if self.dbms == 'MySQL':
                web.dAgent.send("run -d --name {0} -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_DATABASE=root_mysqls mysql".format(
                    web.container_name))
            elif self.dbms == 'Mongo':
                web.db_ctr = web.dAgent.send(
                    "run -d --name {0} mongo".format(web.container_name))
            web.db_ctr = web.dAgent.recv()
            return self.dbms

    def setTheme(self, theme="startbootstrap-agency-1.0.6"):
        if theme == "None":
            Logger.logError("[ERROR] Not supported theme!")
            self.theme = "startbootstrap-agency-1.0.6"
            self.theme_path = os.path.join(THEME_DIR, "themes", self.theme)
            Logger.logInfo("[Info] set theme to {0}!".format(self.theme))
        else:
            self.theme = theme
            self.theme_path = os.path.join(THEME_DIR, "themes", self.theme)
        return self.theme

    def setExpose(self, expose=80):
        if expose == "None":
            Logger.logError("[ERROR] Not supported expose port!")
            self.expose = 80
            Logger.logInfo("[Info] set expose to {0}!".format(self.expose))
        else:
            self.expose = expose
        return self.expose

    def setModules(self, modules="+unfilter"):
        if modules == "None":
            Logger.logError("[ERROR] Not supported modules!")
            self.modules = "+unfilter"
            Logger.logInfo("[Info] set modules to {0}!".format(self.modules))
        else:
            self.modules = modules
        return modules

    def showInfos(self):
        Logger.logInfo("[INFO] Backend: {0}".format(self.backend))
        Logger.logInfo("[INFO] Dbms: {0}".format(self.dbms))
        Logger.logInfo("[INFO] Theme: {0}".format(self.theme))
        Logger.logInfo("[INFO] Expose Port: {0}".format(self.expose))
        Logger.logInfo("[INFO] Color: {0}".format(str(bool(self.color))))
        Logger.logInfo("[INFO] Verbose: {0}".format(str(bool(self.verbose))))
        Logger.logInfo("[INFO] Modules: {0}".format(self.modules))

    def parse(self, arg):
        from core.attack import attack
        arg = arg.strip()
        try:
            if arg.startswith("help"):
                arg = arg[4:].strip()
                for case in switch(arg):
                    if case('set'):
                        Logger.logSuccess("[*] set A = B")
                        break
                    if case('unset'):
                        Logger.logSuccess("[*] unset A")
                        break
                    if case('show'):
                        Logger.logSuccess("[*] show [modules, themes, infos]")
                        break
                    if case():
                        Logger.logSuccess("[*] help [set, unset, show]")
                return True
            elif arg.startswith("set"):
                arg = arg[3:].strip()
                list = re.split("[\s=]+", arg)
                return getattr(self, ''.join(['set', list[0].capitalize()]))(list[1])
            elif arg.startswith("unset"):
                arg = arg[5:].strip()
                print arg
                setattr(self, arg, None)
                return True
            elif arg.startswith("show"):
                arg = arg[4:].strip()
                for case in switch(arg):
                    if case('modules'):
                        Logger.logSuccess(u"{0}".format(
                            u", ".join(attack.modules)))
                        break
                    if case('themes'):
                        Logger.logSuccess(u"{0}".format(
                            u", ".join(attack.themes)))
                        break
                    if case('infos'):
                        Logger.logSuccess("Backend: {0}".format(self.backend))
                        Logger.logSuccess("Dbms: {0}".format(self.dbms))
                        Logger.logSuccess("Theme: {0}".format(self.theme))
                        Logger.logSuccess(
                            "Expose Port: {0}".format(self.expose))
                        Logger.logSuccess(
                            "Color: {0}".format(str(bool(self.color))))
                        Logger.logSuccess("Verbose: {0}".format(
                            str(bool(self.verbose))))
                        Logger.logSuccess("Modules: {0}".format(self.modules))
                        break
                    if case():
                        Logger.logSuccess("[*] show [modules, themes, infos]")
                return True
            elif arg.startswith("start"):
                gen.setThemeEnv()

                self.fp.observer.start()
                try:
                    self.start()
                except (KeyboardInterrupt, SystemExit, RuntimeError):
                    Logger.logInfo("[INFO] See you next time.")
                except APIError as e:
                    Logger.logError("\n" + "[ERROR] " + str(e.explanation))
                    Logger.logInfo(
                        "\n[INFO] Taking you to safely leave the program.")
                finally:
                    self.fp.observer.stop()
                    self.fp.observer.join()
                    self.fp.rmtree(self.fp.path)
                    web.dAgent.send("rm -f {0}".format(web.db_ctr))
                    web.dAgent.send("rm -f {0}".format(web.ctr))

                    gen.reset()
                    self.fp.cleanObserver()
                return True
            elif arg.startswith("CTRL+D"):
                return "CTRL+D"
        except AttributeError as e:
            Logger.logError(e)
            return True

    def bindsOperation(self):
        binds = {
            "{0}".format(web.path): {
                'bind': '{0}'.format(self.mount_point),
                'mode': 'rw',
            },
            "{0}".format(os.path.join(web.path, 'php.ini')): {
                'bind': '/etc/php5/conf.d/php.ini',
                'mode': 'ro'
            },
            "{0}".format(os.path.join(web.path, 'mongodb.so')): {
                'bind': '/usr/lib/php5/modules/mongodb.so',
                'mode': 'ro'
            } if self.dbms == 'Mongo' else None
        }
        return {k: v for k, v in binds.items() if v}

    def start(self):
        path = self.generate()
        web.path = path
        if web.payloads is not None:
            if self.dbms:
                if self.dbms == 'Mongo':
                    cmd = "run -id -p {0}:80 -v {1}:{2}:rw -v {3}:/etc/php5/fpm/php.ini:ro -v {4}:/usr/lib/php5/modules/mongodb.so:ro --link {5}:{6} --name VW --workdir {2} {7} ".format(
                        self.expose, web.path, self.mount_point, os.path.join(web.path, 'php.ini'), os.path.join(web.path, 'mongodb.so'), web.container_name, self.dbms.lower(), self.image)
                else:
                    cmd = "run -id -p {0}:80 -v {1}:{2} -v {3}:/etc/php5/fpm/php.ini --link {4}:{5} --name VW --workdir {2} {6} ".format(
                        self.expose, web.path, self.mount_point, os.path.join(web.path, 'php.ini'), web.container_name, self.dbms.lower(), self.image)
                if self.command:
                    cmd = cmd + self.command
                web.dAgent.send(cmd)
            else:
                cmd = "run -id -p {0}:80 -v {1}:{2}:rw -v {3}:/etc/php5/fpm/php.ini:ro --name VW --workdir {2} {4} ".format(
                    self.expose, web.path, self.mount_point, os.path.join(web.path, 'php.ini'), self.image)
                if self.command:
                    cmd = cmd + self.command
                web.dAgent.send(cmd)
            web.ctr = web.dAgent.recv()

            if "cmd" in web.payloads:
                Logger.logInfo(
                    "[INFO] " + "CMD: {0}".format(web.payloads['cmd']))
                web.dAgent.send(
                    "exec {0} -- {1}".format(web.ctr, web.payloads['cmd']))
            if "warning" in web.payloads:
                for warning in web.payloads['warning']:
                    Logger.logWarning("[WARNING] " + warning)
            if "error" in web.payloads:
                for error in web.payloads['error']:
                    Logger.logError("[ERROR] " + error)

            url = ['http', '127.0.0.1:{0}'.format(
                self.expose), '/', '', '', '']
            params = {}

            if web.payloads['key'] is not None:
                for index, _ in enumerate(web.payloads['key']):
                    if re.search("page", web.payloads['key'][index], flags=re.IGNORECASE):
                        web.payloads['value'][index] = "index"
                    params.update({'{0}'.format(web.payloads['key'][index]): '{0}'.format(
                        web.payloads['value'][index])})

            query = params

            url[4] = urlencode(query)

            t = Terminal()
            with t.location(0, t.height - 1):
                Logger.logSuccess(
                    t.center(t.blink("Browse: {0}".format(urlparse.urlunparse(url)))))

            web.dAgent.send("logs {0} -f".format(web.ctr))


def cli(options=None):
    try:
        if options is None:
            usage = "usage: %prog [options]"
            p = optparse.OptionParser(usage=usage, version="VWGen v0.2.0")
            p.add_option('--console', '-c',
                         action="store_true", metavar='CONSOLE',
                         help="enter console mode")
            p.add_option('--backend',
                         action="store", dest="backend", type="string", default="php", metavar='BACKEND',
                         help="configure the backend (Default: php)")
            p.add_option('--theme',
                         action="store", dest="theme", type="string", default="startbootstrap-agency-1.0.6", metavar='THEME',
                         help="configure the theme (Default: startbootstrap-agency-1.0.6)")
            p.add_option('--expose',
                         action="store", dest="expose", type="int", default=80, metavar='EXPOSE_PORT',
                         help="configure the port of the host for container binding (Default: 80)")
            p.add_option('--database', '--db',
                         action="store", dest="dbms", type="string", default=None, metavar='DBMS',
                         help="configure the dbms for container linking")
            p.add_option('--modules',
                         action="store", dest="modules", default="+unfilter", metavar='LIST',
                         help="list of modules to load (Default: +unfilter)")
            p.add_option('--color',
                         action="store_true", dest="color",
                         help="set terminal color")
            p.add_option('--verbose', '-v',
                         action="store_true", dest="verbosity", metavar='LEVEL',
                         help="set verbosity level")
            group = optparse.OptionGroup(
                p, 'Under development', 'Following options are still in development!')
            group.add_option('--file',
                             action="store", dest="inputFile", type="string", default=None, metavar='FILENAME',
                             help="specify the file that VWGen will gonna operate on")
            p.add_option_group(group)
            options, _ = p.parse_args()
            options = vars(options)

        gen = VWGen()

        if options["console"]:
            enter_shell(gen)
        else:
            if options["inputFile"] is not None:
                web.fp.processInputFile(options["inputFile"])
                from core.customization.instanceSample import instanceSample
                instance = instanceSample(gen)
                instance.main()
                web.fp.customizationClass = instanceSample
                instance.gen_instance.setThemeEnv()

                web.fp.observer.start()
                try:
                    instance.gen_instance.start()
                except (KeyboardInterrupt, SystemExit, RuntimeError):
                    Logger.logInfo("[INFO] See you next time.")
                except APIError as e:
                    Logger.logError("\n" + "[ERROR] " + str(e.explanation))
                    Logger.logInfo(
                        "\n[INFO] Taking you to safely leave the program.")
                finally:
                    web.fp.observer.stop()
                    web.fp.observer.join()
                    web.fp.rmtree(web.fp.path)
                    if web.db_ctr:
                        web.dAgent.send("rm -f {0}".format(web.db_ctr))
                    web.dAgent.send("rm -f {0}".format(web.ctr))

                    web.fp.finishProcessInputFile()
                    raise SystemExit

            if options["color"]:
                gen.setColor()

            if options["verbosity"]:
                gen.setVerbose()

            gen.setBackend(options["backend"])
            gen.setDbms(options["dbms"])
            gen.setTheme(options["theme"])
            gen.setExpose(options["expose"])
            gen.setModules(options["modules"])
            gen.setThemeEnv()

            web.fp.observer.start()
            try:
                gen.start()
            except (KeyboardInterrupt, SystemExit, RuntimeError):
                Logger.logInfo("[INFO] See you next time.")
            except APIError as e:
                Logger.logError("\n" + "[ERROR] " + str(e.explanation))
                Logger.logInfo(
                    "\n[INFO] Taking you to safely leave the program.")
            finally:
                web.fp.observer.stop()
                web.fp.observer.join()
                web.fp.rmtree(web.fp.path)
                if web.db_ctr:
                    web.dAgent.send("rm -f {0}".format(web.db_ctr))
                web.dAgent.send("rm -f {0}".format(web.ctr))
    except (KeyboardInterrupt, SystemExit):
        pass
    except RuntimeError:
        if web.db_ctr:
            web.dAgent.send("rm -f {0}".format(web.db_ctr))
        web.dAgent.send("rm -f {0}".format(web.ctr))

if __name__ == "__main__":
    cli()
