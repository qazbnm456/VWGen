#!/bin/bash

# /Users/boik/Documents/VWGen/VWGen.py --file=/Users/boik/Documents/VWGen/examples/2016_hitcon_training_web_security_advanced/pre-exam/pre-exam.py
docker run --name preexam_myadmin -d --link MySQL_ctr:mysql -e PMA_HOST=mysql -p 8079:80 phpmyadmin/phpmyadmin # root:root_password

# Step ( There are two flags in this challenge. )
# 1. .git/ can fetch all source code, or you can use source.php to read all files( Found by investigating /robots.txt, and $_GET['test'] == 'QNKCDZO' ).
# 2. Then with two methods mentioned above, you can grab the flag from flag.php. ( This is the first flag. )
# 3. We want to find out the second flag, however we know it resides in the / directory, which is not possible to fetch it directly from aforementioned two methods. ( ini_set("open_basedir", '.'); )
# 4. Therefore, we must get to RCE to read any files.
# 5. There are also two ways to get to RCE. 
#    1. The first method is to utilize the php session file by LFI loophole. This loophole happened to 4dm1n panel, and you can access this panel with "admin' and 1=1-- :123". After entering the panel, you should be able to discover the parameter boom is strange with value '4dm1n_home.', and you can also find out the detailed implementation in 4dm1n.php. The explitation is: /index.php?op=4dm1n&boom=/tmp/sess_123&cmd=phpinfo();
#    2. https://github.com/p4-team/ctf/tree/master/2016-04-15-plaid-ctf/web_pixelshop