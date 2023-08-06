
# About lsbatch

**lsbatch** is a [LeadSquared](https://www.leadsquared.com/) provided Batch Jobs software development kit. This allows developers to code and test Batch Jobs offline. It can also be used to prepare final deliverable that can uploaded to configure Batch Jobs in user's LeadSquared account.

## Getting Started

Assuming that you have Python 3.7 and virtualenv installed, install `lsbatch`

```bash
pip install lsbatch
```

## Usage

### Initiate a new Batch Job project

To create a new Batch Job in your local machine, execute the following command in cmd or shell:

```bash
lsbatch init
```

You will be asked to provide name of this Batch Job

```bash
>Your Batch Job Name:
```

A new folder with the provided name will be created in the current directory. 
This folder will be having all the libraries required for Batch Jobs local development.
You will find custom virtualenv in folder name `batch-virtualenv` with following default packages already installed

* boto3==1.14.33
* mysql-connector-python==8.0.21
* pysftp==0.2.9
* sendgrid==6.4.4
* pandas==1.1.0
* pyyaml==5.3.1
* openpyxl==3.0.4
* requests==2.24.0
* tabulate==0.8.7
* numpy==1.19.1

*After initiating batch with `lsbatch init` ,  make sure all the following commands are executed at the project folder level*

```bash
cd {batch_job_folder_name}
```

# General rules for writing a Batch Job

1. Your Batch Job folder should have a folder by name `src` which will be used to write your actual code. This folder is automatically created during the `init` process
2. User should keep their Batch Job files in 'src' folder only
3. `src` folder should have `main.py` file that is basically the starting point of your application. By default this file is created with sample code during the `init` process
3. Your src folder may contain a requirements.txt file which can be used to provide any custom packages which you may require

### Using inbuilt Batch Jobs function

Batch Job provides various functions for comman tasks like logging, sending notification emails or making DB queries. `lsbatch` packs and mocks the same functions and are listed below:

#### Logging
``` 
LS.log.info('Hello')
LS.log.info('Hello', {"Support Email": "support@leadsquared.com"})
LS.log.info(LS.settings.mykey)
LS.log.debug('Debug Log Example')
LS.log.error(type(err).__name__, traceback.format_exc())
LS.log.fatal(type(err).__name__, traceback.format_exc())
```
#### Using Variable
Used to store key/value pair with sensitive/private data. For example API key for some third party service or your SFTP password. It can be retrieved using following key
``` 
LS.settings.<key_name>
```

#### Send Batch Job status notification email
```
LS.email.send_email_notification(<EmailType>, <Subject>, <EmailBody>, isHTML =<True/False>)
```
Where
* EmailType: one of "Success" or "Failure" which corresponds to success or failure of execution status
* Subject: can be maximum 255 character, above which it will be trimmed
* EmailBody: plain text or HTML content
* isHTML: is an optional parameter with default value as True

#### Making DB Calls
You can connect to your LeadSquared account database and ETL database as well. Use the following function to query the same
```
LS.db.execute_DB_query(<query>, multi=False)
LS.db.execute_ETL_query(<query>, multi=False)
```
by default the function considers the query are single statement. For multiline query, pass `multi` parameter as `True`

**Mocking DB query result**
To mock the DB result use the file `query.json` which is provided in the root project folder. It contains a json where 
* key is the DB query(exact - case sensitive) and 
* value is the csv file name that contains the result. 

You will also find a `sample_query_result.csv` in project's root folder which is mapped as sample response in `query.json`.

You can create csv file by any name. Please note that this is purely for mocking purpose and does not evaluate the query, syntax or result in any way. Use the admin panel in your LeadSquared account to validate the same.

###	Executing a Batch Job

To run Batch Job, run command `lsbatch run`

```bash
lsbatch run
```
This will execute the code in context of virtual environment that has already been setup

### Install LeadSquared Batch Job dependencies in current folder

The root folder already contains a `.gitignore` file that will commit only necessary files to your source code repository. Feel free to update the file as per your need. If you clone the repository, run the `lsbatch install` command inside the project directory to setup the Batch Job environment again. 

```bash
lsbatch install
```
This command can also be used in existing projects to reset the Batch Jobs environment at any time.

> To run this command succesfully, current directory should have `src` that contains your code 

### Install your custom packages

```bash
lsbatch install {package_name}
```

This installs your custom package to `batch-virtualenv` folder. Also it creates/updates a `requirements.txt` file inside `src` folder. `requirements.txt` file will be used to identify dependencies at the time of actual execution of the Batch Job

### Packaging your project for deployment

Batch Job accepts the deliverables as a zip file. To zip the project in a correct way, execute the following command

```bash
lsbatch pack
```

This will create a `code.zip` file in the directory named `deliverables`. Remember to add this directory to the `.gitignore` file in order to reduce the size of repository


### Uninstall package

To uninstall a custom package, execute the following command

```bash
lsbatch uninstall {package_name}
```
This will also remove the package name from `requirements.txt` file


#### Configuring Tenant Profile

You can create multiple tenant profiles with various access levels using the configure command

```sh
$ lsbatch configure
```
You will be prompted to enter
* Profile Name : Define the profile name. We suggest you to enter a profile name in the following convention, so that it is easy to remember and re-use - <orgcode>+<developer access level> (e.g., 1234Admin)
* Orgcode : LeadSquared organization code (e.g., 1234). To find your orgcode, see How to Find My LeadSquared Orgcode.
* Region : You may pass 1, 11, or 21. Alternatively, you can pass SGP, US, or MUM.
1 denotes Singapore | 11 denotes U.S.A | 21 denotes India.
* Token : Pass the token generated from the Batch Jobs UI.

You can also simply run lsbatch, it will prompt all available commands

```sh
$ lsbatch
```


#### Create and Upload a Batch Job Code for Deployment

To learn how to upload the batch job code directly from the LeadSquared UI, see [Create a Batch Job](https://apidocs.leadsquared.com/create-a-batch-job/)

Pass the command line parameters --orgcode --region --token. You may also pass these parameters as -o, -r and -t.

E.g.
```sh
$ lsbatch save --orgcode 1234 --region 1 --token asdfghijkl1234
```

Alternatively, if you've configured a profile use --profile or -p.

E.g.
```sh
$ lsbatch save --profile mytenant1234
```

##### Note:

* If the Batch Job Id doesn't exist in the batch_details.json file, the command creates a Batch Job and uploads the code.
* If the Batch Job Id exists in batch_detals.json, it packs and uploads the code to the respective Batch Job.

To save the settings, pass command line parameter --settings, or -s.

E.g.
```sh
$ lsbatch save --profile mytenant1234 --settings
```

**Note**: Only Admins and Developer-Configurator can save the settings.


#### Deploy or Publish a Batch Job

The following command publishes a Batch Job.

Pass the command line parameters --orgcode --region --token. You may also pass these parameters as -o, -r and -t.

E.g.
```sh
$ lsbatch publish --orgcode 1234 --region 1 --token asdfghijkl1234
```

Alternatively, if you've configured a profile use --profile or -p.

E.g.
```sh
$ lsbatch publish --profile mytenant1234
```

**Note**: Only Admins can publish a Batch Job.