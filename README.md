# Implementing Docker Microservices Architecture - Assignment No.9:

## Student Service:
This repository contains the implementation of a microservice, named `student`, designed for managing student data within a university system. It utilizes a Dockerized environment for easy deployment and scalability. The microservice is part of a larger system that includes a server and an Nginx reverse proxy for handling requests.

## Overall Service Architecture
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/742d9296-bea8-4e9e-9054-62a9699778cc)


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

## Microservice

### Design
Our microservice, forming part of a larger university system, follows a three-layer architectural pattern, composed of the following layers:

- **Application Layer**: This is the top layer where the application logic and the Flask routes are defined. It's responsible for handling HTTP requests and responses, marshalling data, and interfacing with the domain layer for business logic.

- **Domain Layer**: Here lies the core business logic of the microservice. It's responsible for executing operations related to student entities, enforcing business rules, and ensuring data consistency and validity.

- **Data Access Layer**: This layer abstracts the logic for data storage and retrieval. It communicates with the database and performs CRUD (Create, Read, Update, Delete) operations, translating between the database and the domain models.

The microservice is designed to be self-contained, with its own database access, business logic, and application interface. This design allows for independent scaling, development, and deployment of the microservice.

### Functionality

The student microservice offers the following functionalities:

- **Add Student**: Adds a new student record with fields like name, age, and education level.
- **Modify Student**: Updates an existing student's data using the student ID.
- **Get Student**: Retrieves information for a specific student using their student ID.
- **Get All Students**: Fetches details of all students.
- **Delete Student**: Removes a student's record from the system using their student ID.

Below is an explanation of the key components of its `Dockerfile`:
```
# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

## Server
The server component of our architecture acts as a gateway, interfacing with the client-side applications and the internal microservice responsible for student data management. It is designed to forward requests and aggregate responses, providing a cohesive API endpoint for client applications.
The server provides a unified API endpoint that encapsulates internal microservice calls. It abstracts the complexity of the microservice architecture from the client, simplifying client integration and allowing for future scalability and modifications without affecting the client applications.


### API Endpoints
The server exposes several endpoints that interact with the microservice, which in turn manages student data:

- `POST /student`: Adds a new student.
- `PUT /student`: Modifies an existing student.
- `GET /student`: Retrieves a student's information.
- `DELETE /student`: Deletes a student record.
- `GET /students`: Retrieves information for all students.

Below is an explanation of the key components of its `Dockerfile`:
```
# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
```

Additionally, `server` communicates with the `microservice` through the `Nginx` reverse proxy as demonstrated in the following:
`MICROSERVICE_BASE_URL variable is set to "http://nginx:80`

## Nginx
The Nginx service in our architecture acts as a reverse proxy, efficiently managing and routing incoming HTTP requests to the appropriate backend service. The configuration for the Nginx service is designed to ensure optimal load distribution and seamless forwarding of client requests to the `microservice`. Below is an explanation of the key components of its `Dockerfile`:

```
events {}

http {
    upstream backend {
        least_conn;
        server microservice:5000;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
Following is the algorithm used to perform load balancing:

**Least Connections (least_conn)**: This algorithm directs traffic to the backend server with the fewest active connections. It's particularly useful in scenarios where the request load is unevenly distributed and some requests take longer to process than others. When a new request comes in, Nginx evaluates all the servers in the `upstream` block and forwards the request to the one with the least number of active connections.

## Database
The microservice leverages a PostgreSQL database to store and manage student data. The connection and table schema are defined as follows:

| **Parameter** | **Value** | **Description**                                |
|---------------|-----------|------------------------------------------------|
| database      | postgres  | The default database provided by PostgreSQL.   |
| user          | postgres  | Default PostgreSQL user.                       |
| password      | 1qaz2wsx@ | Password for the PostgreSQL user.              |
| host          | postgres  | Hostname for the PostgreSQL service in Docker. |
| port          | 5432      | Default port for PostgreSQL.                   |

### Student Table Schema
The student table is structured with the following columns:

| Column            | Type                     | Constraints         |
|-------------------|--------------------------|---------------------|
| `id`              | `SERIAL`                 | `PRIMARY KEY`       |
| `name`            | `VARCHAR(100)`           |                     |
| `age`             | `INT`                    |                     |
| `student_id`      | `VARCHAR(50)`            | `UNIQUE`            |
| `education_level` | `VARCHAR(50)`            |                     |

`education_level` must be either `undergraduate`, `graduate`, or `phd`.

## Docker Configuration
In this project, Docker orchestrates a microservice architecture, ensuring each component is containerized for easy deployment and isolation. Docker Compose manages the multi-container setup, enabling smooth inter-service communication, consistent environments, and facilitating scaling of services to meet demand.
The `Dockerfile` is a text document containing all the commands a user could call on the command line to assemble an image. In this project, Dockerfiles serve as the blueprint for building Docker images for the server, Nginx, and microservice components, ensuring that each service is packaged with its dependencies in a consistent, isolated environment that's ready to be deployed anywhere Docker is running.
The `docker-compose.yml` file is a `YAML` file used by Docker Compose to define and run multi-container Docker applications. With Compose, you use a YAML file to configure your application's services, networks, and volumes. Then, with a single command, you create and start all the services specified in the configuration. Below is our implementation:

```
version: '3'

services:
  nginx:
    build: ./src/nginx
    ports:
      - "7000:80"
    depends_on:
      - server
      - microservice

  server:
    build: ./src/server
    ports:
      - "4000:4000"
    depends_on:
      - postgres

  microservice:
    build: ./src/microservice
    scale: 3
    depends_on:
      - postgres

  postgres:
    image: postgres:latest
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: '1qaz2wsx@'
      POSTGRES_DB: 'postgres'
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Services Configuration
- **nginx**: This service builds the Nginx container from the Dockerfile located in `./src/nginx`. It forwards the host machine's `port 7000` to the container's `port 80`. It depends on the server and microservice, meaning it will wait for these to be available before starting.

- **server**: This service builds the server container from the Dockerfile in `./src/server`. The server's `port 4000` is published to the host machine, allowing external access. It depends on the postgres service, ensuring the database is ready before the server starts.

- **microservice**: The microservice is built from its Dockerfile in `./src/microservice`. The scale: `3` directive tells Docker Compose to start `three instances` of this service, providing scalability. It also depends on the `postgres` service to ensure the database is available before it starts.

- **postgres**: This service uses the `postgres:latest` image from Docker Hub. It maps the default `PostgreSQL port 5432` to the same port on the host, and sets environment variables for the default password and database name. The postgres_data volume is mounted to persist the database data.

### Functionality
The `docker-compose.yml` file defines a complete setup for a microservices architecture, including a web server, an application server, a microservices layer with scaling, and a database with persistent storage. The `depends_on` option is used to manage the order of service startup and dependencies. The ports option maps the containers' ports to the host, enabling external access to the services. The build context points to the location of the Dockerfiles for building the images, and the environment section specifies the necessary environment variables for the containers. The volumes section ensures data persistence for the PostgreSQL database.

## Running the Application

To run the application, use Docker Compose:

``` docker-compose up --build --scale microservice=3```

This command builds the Docker images for each service and starts the containers as defined in docker-compose.yml. Note that the `scale` argument can be dynamically set in each run.
Ourput:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/95fb9980-c4a9-4eaa-abd4-f656fe28ba80)
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/2f71a273-95dc-4e5b-81fa-8ae6f62b990d)

`docker container ls`:
```
CONTAINER ID   IMAGE                       COMMAND                  CREATED         STATUS         PORTS                                       NAMES
8b13c5c9a43d   se-lab-week9_nginx          "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:7000->80/tcp, :::7000->80/tcp       se-lab-week9_nginx_1
b20588b828e3   se-lab-week9_microservice   "flask run --host=0.…"   3 minutes ago   Up 2 minutes   5000/tcp                                    se-lab-week9_microservice_1
62c3e1abf9a5   se-lab-week9_microservice   "flask run --host=0.…"   3 minutes ago   Up 2 minutes   5000/tcp                                    se-lab-week9_microservice_3
ab237634f5ff   se-lab-week9_microservice   "flask run --host=0.…"   3 minutes ago   Up 2 minutes   5000/tcp                                    se-lab-week9_microservice_2
697903e30e8c   se-lab-week9_server         "flask run --host=0.…"   3 hours ago     Up 2 minutes   0.0.0.0:4000->4000/tcp, :::4000->4000/tcp   se-lab-week9_server_1
c51fb4c5880e   postgres:latest             "docker-entrypoint.s…"   4 hours ago     Up 2 minutes   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   se-lab-week9_postgres_1
```

`docker image ls`:
```
REPOSITORY                  TAG       IMAGE ID       CREATED         SIZE
se-lab-week9_microservice   latest    a13ae5772836   5 minutes ago   1.02GB
se-lab-week9_server         latest    bd71eafac0c7   3 hours ago     1.01GB
se-lab-week9_nginx          latest    911c20413f6c   5 hours ago     187MB
```

## Test

Initially, here is the response of the `/students/` API:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/f7e69816-3a34-4ba6-a4ce-a8ce9c7f7c27)


Afterward, we add three students as shown in the following:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/415329d3-5a7c-40d4-aaa4-23836289f04a)
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/1cfa2dde-79dc-4aa0-92e0-68cf93c96176)
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/69219662-5770-45f5-b416-1d464bc34a24)

Subsequently, we call the `/students/` API again:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/51f59937-02c0-4c51-a834-5e86da255b2c)

Additionally, we call the `/student GET API` for Alireza Heidari:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/4091fec1-0936-4147-b22c-2a5592e5b8b5)

Next, we modify the age of Hamidreza and set it to 23:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/4f4f214b-e81b-4ca6-b85e-1f8d393a2b48)
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/78695dca-fc33-4c9b-bc98-06fea25673bc)

Finally, we delete Alireza Heidari's record:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/72fb07b1-c7e0-42bf-b860-72cca3435121)
![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/7a2549ca-5d9c-4fa1-ad86-bd7ce442f10e)

Also, here is a shot from the container's logs:

![image](https://github.com/alirezaheidari-cs/SE-Lab-Week9/assets/59364943/7bf57d94-f6eb-458d-8b86-bf3b80b82519)



## Question: What does "stateless" mean and how have we utilized this concept in our experiment?

Stateless architecture is a design approach where each request to a server contains all the necessary information to complete the request, without requiring the server to retain user or session information between requests. This design leads to systems that are easier to scale and maintain.

In our project, we've embraced statelessness in several ways:

- Our use of the HTTP protocol, which doesn't retain session state between requests, means each request is independent and must be complete in itself.
- The Nginx load balancer treats each request as an independent transaction, using the `least_conn` algorithm to distribute requests evenly across available microservice instances without considering the state of previous interactions.
- The microservices themselves are designed to be stateless. They handle requests independently of each other, ensuring that any instance can respond to any request, which is a key feature for scaling services horizontally.
- Interactions with the PostgreSQL database are stateless, with each query containing all the information needed without depending on previous interactions, thus enhancing performance and reliability.
