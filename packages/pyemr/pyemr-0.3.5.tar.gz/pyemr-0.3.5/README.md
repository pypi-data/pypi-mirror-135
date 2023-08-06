<br><br>


<img src='.media/logo.png' style='width:400px; float:left'>
<br>

# PYEMR : 
<br><br>


## Python EMR Toolkit

A command line tool for developing, testing and packaging pyspark applications on EMR.

<br> 
<p align="center">
<img src='.media/code.png' style='width:350px;'>
</p>

### Features: 

- Easily submit Spark scripts along with any dependencies
- Develop spark scripts locally with automatic s3 mocking.
- Export scripts/packages as Airflow dag
- Shortcuts for viewing logs, ssm and cancelling steps 
- The outputs are standalone. Pyemr is never needed as a dependency in production code.

<br>
<br>





# Video Tutorial

<br>

<p align="center" style='padding:10%'>
	<a href='https://youtu.be/z_y5YrE8r9I'>
	<img src='.media/youtubevideo.png' style='width:90%;'>
</p>

<br>
<br>


# Quick Start

### Notebook

Launch a jupyter notebook with s3-mocking, 

```
pyemr notebook 
```

Then select the the PYEMR Kernel from the dropdown. 

<p align="center" style='padding:10%'>
	<img src='.media/notebook_kernel.png' style='width:50%;'>
</p>


### Packages

To create a spark package,

1. Init the project config [toml](https://python-poetry.org/).  
```
pyemr init 
```
Add python dependency,
```
poetry add <some_package_dependency>
```
2. Create a script and test it, 
```
pyemr test src/script.py
```
3.  Then build and push the package to s3, 
```
pyemr build 
```
( NOTE: The first time you run this its building the docker image from scratch. This might take > 5 min.)

4. Submit to the cluster, 
```
pyemr submit src/script.py --arg 1
```

5. Create airflow dag, 
```
pyemr export src/script.py --arg 1
```

<br>
<br>

# Usage

<br>

### 0. Install 

- Install docker [Docker](https://docs.docker.com/desktop/mac/install/). 
- Install pyemr
```
pip install pyemr 
```
- install enchant (optional)
```brew install enchant```

<br>

### 1. Init
Init creates a ['pyproject.toml'](https://stackoverflow.com/questions/62983756/what-is-pyproject-toml-file-for). It can be run with arguments, 
```
pyemr init \
--project_name=example \
--target_cluster="Cluster Name" \
--s3_stage_dir=s3://some/s3/directory \
--stage=dev \
--region=eu-west-1
```

Alternatively you can run it without arguments and enter configs interactively,
```
pyemr init 
```

- project_name: Project name
- target_cluster: Name of the EMR cluster to use
- s3_stage_dir: s3 path where the scripts and build will be saved
- stage: The development stage [dev/qa/prod]

<br>


### 2. Dependencies
Add dependency to the project,

```
poetry add catboost
```

<br>


### 3. Test
Test a pyspark script, 
```
pyemr test src/script.py
```
This will run the script locally. Paths on s3 will be downloaded and mocked in './data/mock/s3'.

<br>

### 4. Debug

Download master and application logs into './logs/<step_id>'. It also creates a summary of errors,
```
pyemr logs 
```

Specify a specific step
```
pyemr logs <step_id>
```

Print the last n lines of the last steps stderr,
```
pyemr stderr
```

Print the last n lines of the last steps stdout,
```
pyemr stdout 
```

Alternatively you can specify the spark step id, 
```
pyemr stdout <step_id>
```

<br>

### 5. SSM

ssm starts a bash session inside the  cluster master node.  
```
pyemr ssm 
```

Or the master of another cluster, 
```
pyemr ssm <cluster_name>
```

NOTE: This requires your aws account to have the correct permissions. 

<br>

### 6. Local 

Start a jupyter notebook inside a local aws linux container. This includes s3 mocking, 
```
pyemr notebook 
```

Start an interactive python session with s3 mocking, 
```
pyemr python 
```

Start a bash session inside aws linux container, 
```
pyemr bash
```

<br>

### 7. Mock

Downloads part of an s3 folder/table into the mock directory,
```
pyemr mock s3://some/s3/path 
```

Downloads all of a folder/file into the mock directory, 
```
pyemr mock s3://some/s3/path --all
```

<br>


### 8. Tools 

List emr clusters,
```
pyemr clusters
```

List project steps on default cluster, 
```
pyemr steps
```

List all steps,
```
pyemr steps --all
```

List steps on a given cluster, 
```
pyemr steps <cluster_name>
```

Cancel the latest step, 
```
pyemr cancel 
```

Cancel a specified step, 
```
pyemr cancel --step_id <step_id> --cluster_name <cluster_name>
```

<br>

### 9. Export 

Exports the step as an airflow dag, 
```
pyemr export src/script.py --arg 1
```

<br>


### 10. Dev
Format code and remove unused package, 
```
pyemr format 
```

Check for errors,
```
pyemr lint -E
```

Lint and check for style, errors and warnings, 
```
pyemr lint 
```

Spell check docstrings, 
```
pyemr lint -S
```
(To spell check run "brew install enchant")

```
pyemr spellcheck README.md
```


<br> 
<br> 
<br> 
<br> 

------------------------------------------------------

<br> 
<br> 
<br> 
<br> 
<br> 
<br> 
<br> 
<br> 


# Appendix
<br>

### Dependencies
Requires docker.

### Development 

To reformat the code run 
```
pyemr format
```

Lint code,
```
pyemr lint
```

To run local tests, 
```
pip install . 
pytest
```

To run tests including s3 and emr features, 
```
pip install . 
pytest \
	--s3_stage_dir s3://some/staging/path/unittest  \
	--s3_parquet_file s3://some/parquet/table \
	--cluster_name some_cluster_name 
	--region eu-west-1
```


<br> 

### Troubleshoot

#### Error 1:
```
[Errno 28] No space left on device
```

#### Solution: 

```
docker system prune
```

WARNING! This will remove:
- all stopped containers
- all networks not used by at least one container
- all dangling images
- all dangling build cache


```
docker system prune --all --force --volumes
````

<br><br>

####  Error 2:

```
botocore.exceptions.ClientError: An error occurred (InvalidSignatureException) when calling the ListClusters operation: Signature expired: 20211210T145000Z is now earlier than 20211210T145057Z (20211210T145557Z - 5 min.)
```


#### Solution

https://stackoverflow.com/questions/61640295/aws-invalidsignatureexception-signature-expired-when-running-from-docker-contai


#### Error 3:

```
Exception: Unable to find py4j, your SPARK_HOME may not be configured correctly
```

#### Solution

Set the SPARK_HOME e.g, 

```
export SPARK_HOME=/usr/local/Cellar/apache-spark/3.2.0/libexec
```


#### Error 4: 

```
An error occurred while calling o56.load.
: java.lang.reflect.InaccessibleObjectException: Unable to make field private transient java.lang.String java.net.URI.scheme accessible: module java.base does not "opens java.net" to unnamed module @40f9161a
```
#### Solution

switch global java version 
https://github.com/halcyon/asdf-java

```
brew install asdf
```

```
asdf plugin-add java https://github.com/halcyon/asdf-java.git
asdf install java adoptopenjdk-8.0.312+7
asdf global java adoptopenjdk-8.0.312+7
```

Set java home variables in bash/zsh, 
```
. ~/.asdf/plugins/java/set-java-home.bash
. ~/.asdf/plugins/java/set-java-home.zsh
```

#### Error 5: No space left on device
#### Solution 

```
# Remove all containers that aren't running.
docker rm -vf $(docker ps -a -q --filter "status=exited")

# Remove untagged images.
docker rmi -f $(docker images -q -f "dangling=true")

# Remove unused volumes using "rm" or "prune".
docker volume rm -f $(docker volume ls -f "dangling=true")
docker volume prune -f

# Remove unused networks.
docker network prune -f
```

#### Error 6: docker crashes. or build freezes 
```
killall Docker && open /Applications/Docker.app
```

Start it again from the desktop app. 

#### Error 7: build test fails
This might be because one of the ports is being used, or a pyemr container is still running. Try, 

```
docker container ls
```
Then stop the container
```
docker stop <container id>
```



## TODO:
- Add other spark version support
- Support EMR docker containers 
- Add a unittests for 'pyemr notebook' in docker env. 
- Remove additional koalas dependencies when working with pyspark 3
- Add spark config parameters in the toml and submit methods
