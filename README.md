# Vulnerable Web applications Generator

This is the Git repo of the `VWGen`, which stands for *Vulnerable Web applications Generator*.

**Relevant links:**
 [Github](https://github.com/qazbnm456/VWGen)

---------------------------------------

**Table of contents**

 * [Releases](#releases)
 * [Status quo](#status)
 * [Feature](#feature)
 * [Install](#install)
 * [Instruction](#instruction)
 * [In Brief](#brief)
 * [Know issues](#issue)
 * [Contributing](#contribute)
 * [LICENSE](#license)

---------------------------------------

<a name="releases"></a>
## Releases

- 0.1.0 -- Initial release
- 0.2.0 -- Now, VWGen can also be one of [Tsaotun](https://github.com/qazbnm456/tsaotun)'s addon. :tada:

<a name="status"></a>
## Status quo

1. Supporting very limited modules, such as [SQLI](https://www.owasp.org/index.php/SQL_Injection), [NOSQLI](https://www.owasp.org/index.php/Testing_for_NoSQL_injection), [LFI](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion), [CRLF](https://www.owasp.org/index.php/CRLF_Injection), [Command Injection](https://www.owasp.org/index.php/Command_Injection) and [XSS](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)).
2. There are two important modules which play essential role in deploying vulnerable web apps.
   - *unfilter* module scrap the sites and find the keywords to be replaced by parameters.
   - *expand* module learn the sites and try to rearrange the elements to let child modules insert their payloads within it.
3. Only two themes right now.
    <div align="center"><img src="http://i.imgur.com/jgdO4HD.png" /></div>
4. Python3 is currently not supported!
5. `--file` option works, but it still needs some developing. Example command: `./VWGen.py --file="$VWGen_HOME/examples/2016_ais3_web3/sample.py"`

<a name="feature"></a>
## Feature

`--file` option makes share web challenges easily. All you need to do is provide a custom script, which defines how vulnerabilities would be made or be triggered, and each one can just load that script to spawn the same vulnerable web applications immediately.

There is a [examples/](https://github.com/qazbnm456/VWGen/tree/master/examples) directory in the root folder, and I will put some sample scripts in it. Now, we have so many scripts!

<a name="install"></a>
## Install

1. Install docker binary. Only versions 1.11.0 above supported. Check out official [installing guide](https://docs.docker.com/linux/).
2. Pull fundamental images that we gonna use with VWGen:
    - `docker pull richarvey/nginx-php-fpm:php5`
    - `docker pull richarvey/nginx-php-fpm:php7`
    - `docker pull mysql:5`
    - `docker pull phpmyadmin/phpmyadmin:4.6.5.1-1`
    - `docker pull node:7`
3. Install:
    - tsaotun: `pip install tsaotun`
    - web.py: `pip install web.py`
    - pycurl: `pip install pycurl`, and if you have error like `Could not run curl-config: [Errno 2] No such file or directory`, solve the problem with `apt-get install libcurl4-openssl-dev`
    - blessed: `pip install blessed`
    - BeautifulSoup 4: `pip install bs4`
    - watchdog: `pip install watchdog`
    - python-prompt-toolkit: `pip install prompt-toolkit`
    - pygments: `pip install pygments`
4. Install lxml: `apt-get install python-lxml` and `pip install lxml`.
5. Clone [VWGen](https://github.com/qazbnm456/VWGen) and type `./VWGen.py --help` or check below for details.

<a name="instruction"></a>
## Instruction

    Usage: VWGen.py [options]

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -c, --console         enter console mode
    --backend=BACKEND     configure the backend (Default: php)
    --theme=THEME         configure the theme (Default: startbootstrap-
                            agency-1.0.6)
    --expose=EXPOSE_PORT  configure the port of the host for container binding
                            (Default: 80)
    --database=DBMS, --db=DBMS
                            configure the dbms for container linking
    --modules=LIST        list of modules to load (Default: +unfilter)
    --color               set terminal color
    -v, --verbose         set verbosity level

    Under development:
        Following options are still in development!

        --file=FILENAME     specify the file that VWGen will gonna operate on

<a name="brief"></a>
## In Brief

Which types of vulnerabilities will be generated would depend on the modules you set while you start VWGen, and following are some screenshots of VWGen:

- `./VWGen.py -c` - Enter console mode.
<div align="center"><img src="http://i.imgur.com/fOZWju1.png" /></div>

- `./VWGen.py` - Start VWGen with some default arguments.
<div align="center"><img src="http://i.imgur.com/55RPixv.png" /></div>

- `./VWGen.py --module="+sqli" --database="MySQL"` - Start VWGen with MySQL based SQL Injection.
<div align="center"><img src="http://i.imgur.com/X5m0OkO.png" /></div>

- `./VWGen.py --module="+exec"` - Start VWGen with command injection vulnerability.
<div align="center"><img src="http://i.imgur.com/Rt0er9E.png" /></div>

<a name="issue"></a>
## Known issues

1. [mod_expand.py](https://github.com/qazbnm456/VWGen/blob/master/core/attack/mod_expand.py) can produce defferent extensions, but it still needs user's interaction to modify source code (Warning message is provided).

<a name="contribute"></a>
## Contributing to VWGen

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) |

Wanna enrich the possibilities that VWGen can inspire? Send pull requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](https://github.com/qazbnm456/VWGen/blob/master/LICENSE).
