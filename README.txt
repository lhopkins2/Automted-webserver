Automated Cloud Services Assignment 1

Author- Liam Hopkins
Date- 05/03/2021

This assignment is a fully automated script that launches a single 't2.nano' type instance into a VPC
that contains a public subnet where the webserver is held. All parts of the instance all automatically
generated although you are provided with the key 'lhkey1.pem'. 

Three scripts are included with it:
monitor.sh- monitors instance and gives meta-data
configure.sh- configures the web page
userdata.sh- installs the Apache server to the web app

It can be run multiple times and will create new instances in seperate VPS's but if the bucket is not deleted
before running the script again it will not create a new bucket an instead leave the current bucket
and then put the image object into the bucket if it is not there already.
