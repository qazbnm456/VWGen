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

1. Supporting very limited modules, such as [SQLI](https://www.owasp.org/index.php/SQL_Injection), [NOSQLI](https://www.owasp.org/index.php/Testing_for_NoSQL_injection), [LFI](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion), [CRLF](https://www.owasp.org/index.php/CRLF_Injection) and [Command Injection](https://www.owasp.org/index.php/Command_Injection).
2. There are two important modules which play essential role indeploying vulnerable web apps.
   - *unfilter* module scrap the sites and find the keywords to be replaced by parameters.
   - *expand* module learn the sites and try to rearrange the elements to let child modules insert there payloads within it.
3. Only two themes right now.
    <div align="center"><img src="http://i.imgur.com/goiRccC.png" /></div>
4. Python3 is not supported!

<a name="install"></a>

## Install

1. Install docker binary. Only versions 1.11.0 above supported. Check out official [installing guide](https://docs.docker.com/linux/).
2. Install docker-py: `pip install docker-py`, blessed: `pip install blessed`, and BeautifulSoup 4: `pip install beautifulsoup4`.
3. Install lxml. `sudo apt-get install python-lxml`
4. Clone [VWGen](https://github.com/qazbnm456/VWGen) and type `./VWGen.py --help` or check below for details.

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

        --craft=CRAFTING    craft the loopholes on your own
        --file=FILENAME     specify the file that VWGen will gonna operate on

<a name="brief"></a>

## In Brief

Which types of vulnerabilities will be generated would depend on the modules you set while you start VWGen, and following are some pictures of VWGen:

- `./VWGen.py --help` - Show help message.
<div align="center"><img src="http://i.imgur.com/pewfjhK.png" /></div>

- `./VWGen.py -c` - Enter console mode.
<div align="center"><img src="http://i.imgur.com/Px0DNGD.png" /></div>

- `./VWGen.py` - Start VWGen with some default arguments.
<div align="center"><img src="http://i.imgur.com/55RPixv.png" /></div>

- `./VWGen.py --module="+sqli" --database="MySQL"` - Start VWGen with MySQL based SQL Injection.
<div align="center"><img src="http://i.imgur.com/X5m0OkO.png" /></div>

- `./VWGen.py --module="+exec"` - Start VWGen with command injection vulnerability.
<div align="center"><img src="http://i.imgur.com/Rt0er9E.png" /></div>

<a name="contribute"></a>

## Contributing to VWGen

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.0-blue.svg) |

Wanna enrich the possibilities that VWGen can inspire? Send pull requests or issues immediately!

<a name="license"></a>

## LICENSE

This project use [Apache License, Version 2.0](https://github.com/qazbnm456/VWGen/blob/master/LICENSE).
