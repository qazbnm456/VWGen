# Vulnerable Web applications Generator

This is the Git repo of the `VWGen`, which stands for *Vulnerable Web applications Generator*.

**Relevant links:**
 [Github](https://github.com/qazbnm456/VWGen)

---------------------------------------

##**Table of contents**

####*[Status quo](#status)*
####*[Install](#install)*
####*[Instruction](#instruction)*
####*[In Brief](#brief)*
####*[Contributing](#contribute)*
####*[LICENSE](#license)*

---------------------------------------

<a name="status"></a>
## Status quo

1. Supporting very limited modules, such as [unfilter](https://www.owasp.org/index.php/Injection_Prevention_Cheat_Sheet), [SQLI](https://www.owasp.org/index.php/SQL_Injection), [NOSQLI](https://www.owasp.org/index.php/Testing_for_NoSQL_injection), [LFI](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion) and [CRLF](https://www.owasp.org/index.php/CRLF_Injection).
    <div align="center"><img src="http://i.imgur.com/FXDDWJk.png" /></div>

2. Only two themes right now.
    <div align="center"><img src="http://i.imgur.com/qRNyz0G.png" /></div>
3. Python3 is not supported!

<a name="install"></a>
## Install

1. Install docker binary. Only versions 1.11.0 above supported. Check out official [installing guide](https://docs.docker.com/linux/).
2. Install docker-py. `pip install docker-py`
3. Install lxml. `sudo apt-get install python-lxml`
4. Clone [VWGen](https://github.com/qazbnm456/VWGen) and type `./VWGen.py --help` or check below for details.

<a name="instruction"></a>
## Instruction

    Usage: VWGen.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c, --console         enter console mode
      --expose=EXPOSE_PORT  configure the port of the host for container binding
                            (Default: 80)
      --database=DBMS       configure the dbms for container linking
      --module=LIST         list of modules to load (Default: +unfilter)
      --color               set terminal color

      Not supported:
        Following options are still in development!

        -v, --verbose       set verbosity level
        --file=FILENAME     specify the file that VWGen will gonna operate on

<a name="brief"></a>
## In Brief

Which types of vulnerabilities will be generated would depend on the modules you set while you start VWGen, and following are some pictures of VWGen:

- `./VWGen.py --help` - Show help message.
<div align="center"><img src="http://i.imgur.com/aTowy7Z.png" /></div>

- `./VWGen.py -c` - Enter console mode.
<div align="center"><img src="http://i.imgur.com/lmGJm9L.png" /></div>

- `./VWGen.py` - Start VWGen with some default arguments.
<div align="center"><img src="http://i.imgur.com/Nb8hdqf.png" /></div>

- `./VWGen.py --module="+sqli" --database="MySQL"` - Start VWGen with MySQL based SQL Injection.
<div align="center"><img src="http://i.imgur.com/uReoiLh.png" /></div>

<a name="contribute"></a>
## Contributing to VWGen

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.1-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.1-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.1-blue.svg) |

Wanna enrich the possibilities that VWGen can inspire? Send pull requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](https://github.com/qazbnm456/VWGen/blob/master/LICENSE).
