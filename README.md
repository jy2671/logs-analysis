# Project: Logs Analysis

The project is to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, the code will answer questions about the site's user activity. Below are the questions the reporting tool will answer:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Installing the Virtual Machine

We're using tools called Vagrant and VirtualBox to install and manage the VM. 

********************************

* **Installed Virtual Box**
   
   VirtualBox is the software that actually runs the virtual machine. You can download it from [virtualbox.org](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
   
   I installed VirtualBox 6.0.4
* **Installed Vagrant**

   Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com](https://www.vagrantup.com/downloads.html). 
   
   I installed Vagrant 2.2.3.
   
   `$ vagrant -v`
   
   `Vagrant 2.2.3`
   
   Note: The `Vagrantfile` used in the project is in the repository
* **Download the VM configuration**

   option 1: download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) 
   
   option 2: use Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm.
   
   Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.
* **Start the virtual machine**

   From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

   `$ vagrant up`
* **log in to newly installed Linux VM**

   When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM!

  `$ vagrant ssh`
   
* **The files for the project**

   Inside the VM, change directory to `/vagrant` and look around with `ls`.

   The files you see here are the same as the ones in the `vagrant` subdirectory on your computer (where you started Vagrant from). Any file you create in one will be automatically shared to the other. This means that you can edit code in your favorite text editor, and run it inside the VM.

   Files in the VM's `/vagrant` directory are shared with the `vagrant` folder on your computer. But other data inside the VM is not. For instance, the PostgreSQL database itself lives only inside the VM.
  
* **Download the data**

   Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

   To build the reporting tool, you'll need to load the site's data into your local database. Review how to use the `psql` command in this lesson: ([FSND version](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/96869cfc-c67e-4a6c-9df2-9f93267b7be5/concepts/0b4079f5-6e64-4dd8-aee9-5c3a0db39840))

   To load the data, cd into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.
Here's what this command does:

   * `psql` — the PostgreSQL command line program
   * `-d news` — connect to the database named news which has been set up for you
   * `-f newsdata.sql` — run the SQL statements in the file newsdata.sql
   
   Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.
   
* **Explore the data**
   
   Once you have the data loaded into your database, connect to your database using `psql -d news` and explore the tables using the `\dt` and `\d table` commands and `select` statements.

   * `\dt` — display tables — lists the tables that are available in the database.
   * `\d` table — (replace table with the name of a table) — shows the database schema for that particular table.
   
   Get a sense for what sort of information is in each column of these tables.

   The database includes three tables:

   * The `authors` table includes information about the authors of articles.
   * The `articles` table includes the articles themselves.
   * The `log` table includes one entry for each time a user has accessed the site.
   
   As you explore the data, you may find it useful to take notes! Don't try to memorize all the columns. Instead, write down a      description of the column names and what kind of values are found in those columns.

* **Connecting from your code**
   
   The database that you're working with in this project is running PostgreSQL, like the `forum` database that you worked with in the course. So in your code, you'll want to use the `psycopg2` Python module to connect to it, for instance:

   * `db = psycopg2.connect("dbname=news")`


### Design of the code and how to run it

This code will create a reporting tool that prints out reports based on the data in the "news" database. The reporting tool is a Python program using the `psycopg2` python module to connect to the database:

`conn = psycopg2.connect("dbname=news")`

The reporting tool answers the three questions. Each one of these questions is answered using a single database query. For question 3, I created two new views `log_404` and `log_total` in the database. Here are the commands for creating these two new views in "news":

```sql
CREATE VIEW log_404 AS
SELECT time::DATE, count(*) AS sum404 
FROM log 
WHERE status like '404 NOT FOUND' 
GROUP BY (time::DATE, status);
```

```sql
CREATE view log_total AS
SELECT time::DATE, count(*) AS total 
FROM log 
GROUP BY time::DATE;
```

#### How to run the code

`vagrant@vagrant:/vagrant$ python news.py`
