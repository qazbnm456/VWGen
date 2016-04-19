# Vulnerable Web applications Generator

This is the Git repo of the `VMGen`, which stands for *Vulnerable Web applications Generator*.

**Relevant links:**
 [Github](https://github.com/qazbnm456/VWGen)

---------------------------------------

##**Table of contents**

####*[Status quo](#status)*
####*[Install](#install)*
####*[Instruction](#instruction)*
####*[Contributing](#contribute)*
####*[LICENSE](#license)*

---------------------------------------

<a name="status"></a>
## Status quo

1. Supporting very limited modules, such as [unfilter](https://www.owasp.org/index.php/Injection_Prevention_Cheat_Sheet), [SQLI](https://www.owasp.org/index.php/SQL_Injection), [NOSQLI](https://www.owasp.org/index.php/Testing_for_NoSQL_injection) and [LFI](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion).

2. Only one theme right now.

3. Python3 is not supported!

<a name="install"></a>
## Install

1. Install latest docker binary. Only version 1.11.0 supported. Check out official [installing guide](https://docs.docker.com/linux/).
2. Install webpy: `pip install web.py --user`
3. Install docker-py: `pip install docker-py --user`
4. Install lxml: `sudo apt-get install python-lxml`
5. Clone [VWGen](https://github.com/qazbnm456/VWGen) and type `python VWGen.py --help` for details.

<a name="instruction"></a>
## Instruction

	Usage: VWGen.py [options] arg1 arg2

	Options:
	  -h, --help            show this help message and exit
	  -p PORT, --port=PORT  Configure the port this server to listen on. Default
	                        is 8080.
	  --expose=PORT         Configure the port of the host for container binding.
	                        Default is 80.
	  --database=DBMS       Configure the dbms for container linking
	  --module=MODULES_LIST
	                        List of modules to load. Default is mod_unfilter.
	  -v LEVEL, --verbose=LEVEL
	                        [Not supported yet] Set verbosity level
	  --file=FILENAME       [Not supported yet] Specify the file that VWGen will
	                        gonna operate on

<a name="contribute"></a>
## Contributing to VWGen

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.11.0-blue.svg) |

Wanna enrich the possibilities that VWGen can inspire? Send requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](https://github.com/qazbnm456/VWGen/blob/master/LICENSE).