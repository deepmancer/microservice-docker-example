# Software Engineering Lab - 9th Exp.

## Student Service:
This repository contains the implementation of a microservice, named `student`, designed for managing student data within a university system. It utilizes a Dockerized environment for easy deployment and scalability. The microservice is part of a larger system that includes a server and an Nginx reverse proxy for handling requests.

## Microservice Functionalities
The student microservice offers the following functionalities:

1. Add Student: Adds a new student record with fields like name, age, and education level.
2. Modify Student: Updates an existing student's data using the student ID.
3. Get Student: Retrieves information for a specific student using their student ID.
4. Get All Students: Fetches details of all students.
5. Delete Student: Removes a student's record from the system using their student ID.

## Project Structure

```
.
├── docker-compose.yml
├── src
│   ├── microservice
│   │   ├── application
│   │   ├── config
│   │   ├── data_access
│   │   ├── domain
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── nginx
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── server
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
└── README.md
```
