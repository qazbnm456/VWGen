# -*- coding: utf-8 -*-

try:
    from collections import OrderedDict
except ImportError:  # For Python 2.6, nocover
    from .ordereddict import OrderedDict

ROOT_COMMANDS = OrderedDict([
    ('help', 'Help'),
    ('set', 'Set Varaible'),
    ('unset', 'Unset Varaible'),
    ('show', 'Show Preset'),
    ('start', 'Emit Container')
])

VARIABLES = OrderedDict([
    ('backend', 'Backend'),
    ('dbms', 'DBMS'),
    ('theme', 'Theme'),
    ('expose', 'Expose port'),
    ('color', 'Enable Color Or Not'),
    ('verbose', 'Enable Verbose Or Not'),
    ('modules', 'Modules To Generate')
])

PRESET_OPTIONS = OrderedDict([
    ('themes', 'Show Available Themes'),
    ('modules', 'Show Available Modules'),
    ('infos', 'Show Variables')
])

BOOLEANS = OrderedDict([
    ('1', 'True'),
    ('0', 'False')
])

RECOMMEND_PORTS = OrderedDict([
    ('80', 'Default Web Server Port'),
    ('8080', 'Comman Web Server Port'),
    ('8888', 'Comman Web Server Port'),
])

BACKENDS = OrderedDict([
    ('php', 'PHP Script Language')
])

DATABASES = OrderedDict([
    ('MySQL', 'MySQL Database'),
    ('Mongo', 'Mongodb')
])

MODULES = OrderedDict([
    ('+unfilter', 'Unfilter Vulnerability'),
    ('+expand', 'Expand theme'),
    ('+sqli', 'SQL Injection Vulnerability'),
    ('+nosqli', 'NoSQL Injection Vulnerability'),
    ('+lfi', 'Local File Inclusion Vulnerability'),
    ('+crlf', 'CRLF Injection Vulnerability'),
    ('+exec', 'Command Injection Vulnerability'),
    ('+xss', 'Cross-Site Script Vulnerability')
])

THEMES = OrderedDict([
    ('startbootstrap-agency-1.0.6', 'Agency Theme'),
    ('startbootstrap-clean-blog-1.0.4', 'Clean Blog Theme'),
])
