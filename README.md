# customrestapi
# Task Manager API



## Table of Contents
- [About](#about)
- [System Architecture](#system-architecture)
  - [REST API](#rest-api)



## About 



## System Architecture





### REST API 
This REST API serves as a simple way to create and manage tasks across teams of users. It facilitates the creation, reading, updating and deletion of tasks and users with hash-based authentication and admin permissions.

The technology stack used to create this API includes a Cloud SQL database (GCP), Python and Docker.

Use the following URL API path:

To create an account:

## <POST> /create/user
  
```
JSON body:
{"user_fname": "John", 
"user_lname": "Smith", 
"username": "Jonno", 
"user_password": "password123", 
"user_email": "john.smith@gmail.com"}
```
  
  










#### -----------------------------------------------------------------------




<br><br>
##### Creating the Docker Image
<p align="left">
  <img src="https://www.docker.com/sites/default/files/d8/2019-07/horizontal-logo-monochromatic-white.png" height="40" />
</p>
Create our docker image with the "Dockerfile" from our repository by:

```
docker build -t gcr.io/${USER_ID}/tasks:v1 .
```

List your Docker images to verify.
```
docker images
```




#### Docker Container
<p align="left">
  <img src="https://www.docker.com/sites/default/files/d8/2019-07/horizontal-logo-monochromatic-white.png" height="75" />
</p>

1. Install [Docker](https://docs.docker.com/get-docker/) and verify your installation with ``` docker -v ```
2. Launch the terminal in the library_api folder or direct to this directory.
3. Build the docker image (be sure to include the ". " at the end and to define your username ``` whoami```)

```
docker build -t <your username>/tasks . 
```

4. Run your container:
```
docker run -it -p 5000:5000 <your username>/tasks 
```

This will map port 5000 to the host 5000 in our container. 

5. Access the backend from your browser via ``http://localhost:5000``

More info: [Dockerizing a Node.js web app](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/) 

