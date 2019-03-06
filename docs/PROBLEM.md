Original Use Case
=================

### Context

As mentioned in the README, this tool was originally created purely as a solution for a technical test.

Below are the details of said technical test, as provided by the employer.

#### Use Case: 

* A database upgrade requires the execution of numbered scripts stored in a specified folder, e.g. SQL scripts such as `045.createtable.sql`.
* There may be gaps in the numbering and there isn't always a . (dot) after the number. 
* The database upgrade is based on looking up the current version in the database and comparing this number to the numbers in the script names. 
* If the version number from the db matches the highest number from the script then nothing is executed. 
* If the number from the db is lower than the highest number from the scripts, then all scripts that contain a higher number than the db will be executed against the database. 
* In addition, the database version table is updated after the install with the highest number. 


#### Requirements:

* Supported Languages: Bash, Python2.7, PHP, Shell, Ruby, Powershell
  * No other languages will be accepted
* The table where the version is stored is called 'versionTable', and the row with the version is 'version'.
  * This table contains only one column with the actual version.
* You will have to use a MySQL database.
* The information about the database and the directory will be passed 
through arguments, following this format:
  ```
  <directory with .sql scripts> <username for the DB> <DB host> <DB name> <DB password>
  ```
 

#### Task:

How would you implement this in order to create an automated solution to the above requirements?

Please send us your script(s) and any associated notes for our review and we will come back to you asap regarding next steps.

**Important:** the documentation you compile is as important as the quality of the script.

