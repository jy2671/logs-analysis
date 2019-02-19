## Project: Logs Analysis

The project is to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the code will answer questions about the site's user activity

### Installing the Virtual Machine

We're using tools called Vagrant and VirtualBox to install and manage the VM. 

********************************

* **Installed Virtual Box**
VirtualBox 6.0.4
* **Installed Vagrant**
`$ vagrant -v`
`Vagrant 2.2.3`
* **Download the VM configuration**
option 1: download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) 
option 2: use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
* **Start the virtual machine**
`$ vagrant up`
* **log in to newly installed Linux VM**
`$ vagrant ssh`

### Design of the code and how to run it

This code will create a reporting tool that prints out reports based on the data in the "news" database. The reporting tool is a Python program using the `psycopg2` python module to connect to the database:

`conn = psycopg2.connect("dbname=news")`

The reporting tool answers the three questions. Each one of these questions is answered using a single database query. For question 3, I created two new views `log_404` and `log_total` in the database. Here are the commands for creating these two new views in "news":

`create view log_404 as`
`select time::DATE, count(*) as sum404 from log where status like '404 NOT FOUND' group by (time::DATE, status);`

`create view log_total as`
`select time::DATE, count(*) as total from log group by time::DATE;`

***how to run the code***

`vagrant@vagrant:/vagrant$ python news.py`
