# 🏛️ Microservices Architecture for University Student Management

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/NGINX-009639.svg?style=for-the-badge&logo=NGINX&logoColor=white" alt="NGINX">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white" alt="Docker">
</p>

Welcome to the **Microservices Architecture** project! This repository hosts a `Student Service` microservice, built to efficiently manage student data within a university system. This service is Dockerized for seamless deployment and scalability, and is part of a larger system architecture that includes a server and an Nginx reverse proxy.

---

## 📐 Overall Service Architecture
![Service Architecture Diagram](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/742d9296-bea8-4e9e-9054-62a9699778cc)

## 🗂️ Project Structure

Here's a quick overview of the project structure:

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

## 🛠️ Microservice Design

This microservice is a self-contained component within the larger university system, designed using a **three-layer architecture**:

- **🖥️ Application Layer**: Manages the application logic, Flask routes, and handles HTTP requests/responses.
- **🧠 Domain Layer**: Houses the core business logic, handling operations related to student entities and ensuring data consistency.
- **💾 Data Access Layer**: Abstracts the data storage/retrieval logic, managing CRUD operations with the database.

### ✨ Key Features
The Student microservice offers the following capabilities:

- **Add Student**: Create a new student record.
- **Modify Student**: Update existing student details.
- **Get Student**: Retrieve a student's details by their ID.
- **Get All Students**: Fetch a list of all students.
- **Delete Student**: Remove a student's record from the system.

### 🐳 Dockerfile Breakdown

Here’s a quick glance at the key components of the `Dockerfile` used to containerize this microservice:

```Dockerfile
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

## 🌐 Server Component

The server acts as a gateway, handling client requests and coordinating with the microservice for student data management. It simplifies client interactions by providing a unified API endpoint.

### 📬 API Endpoints

- `POST /student`: Adds a new student.
- `PUT /student`: Modifies existing student details.
- `GET /student`: Retrieves a student’s information.
- `DELETE /student`: Deletes a student record.
- `GET /students`: Retrieves information for all students.

### 🐳 Dockerfile Breakdown

```Dockerfile
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

## 🌍 Nginx Configuration

The Nginx service acts as a reverse proxy, efficiently routing incoming HTTP requests to the appropriate backend service. It is configured to ensure optimal load balancing and seamless request forwarding.

### 🔄 Load Balancing

**Least Connections (least_conn)**: This algorithm directs traffic to the backend server with the fewest active connections, ensuring efficient load distribution.

### 🐳 Nginx Dockerfile

```nginx
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

## 🗄️ Database Configuration

The microservice uses a PostgreSQL database to manage student data.

### 📋 Student Table Schema

| Column            | Type            | Constraints     |
|-------------------|-----------------|-----------------|
| `id`              | `SERIAL`        | `PRIMARY KEY`   |
| `name`            | `VARCHAR(100)`  |                 |
| `age`             | `INT`           |                 |
| `student_id`      | `VARCHAR(50)`   | `UNIQUE`        |
| `education_level` | `VARCHAR(50)`   |                 |

`education_level` must be either `undergraduate`, `graduate`, or `phd`.

## 🐳 Docker Configuration

This project uses Docker and Docker Compose to orchestrate the microservice architecture, ensuring each component is containerized for easy deployment and isolation.

### 📦 Docker Compose Setup

```yaml
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

### ⚙️ Running the Application

To run the application, simply use Docker Compose:

```bash
docker-compose up --build --scale microservice=3
```

This command will build the Docker images for each service and start the containers as defined in `docker-compose.yml`. The `scale` argument can be adjusted to control the number of microservice instances.

## ✅ Testing the Microservice

Here’s how the application works in action:

1. **Initial API Call** - Fetch all students:
   ![Initial API Call](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/f7e69816-3a34-4ba6-a4ce-a8ce9c7f7c27)

2. **Adding Students** - Add three students:
   ![Add Student 1](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/415329d3-5a7c-40d4-aaa4-23836289f04a)
   ![Add Student 2](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/1cfa2dde-79dc-4aa0-92e0-68cf93c96176)
   ![Add Student 3](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/69219662-5770-45f5-b416-1d464bc34a24)

3. **Fetch All Students** - Call the `/students/` API again:
   ![Fetch All Students](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/51f59937-02c0-4c51-a834-5e86da255b2c)

4. **Fetch Single Student** - Get details of a specific student:
   ![Fetch Single Student](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/4091fec1-0936-4147-b22c-2a5592e5b8b5)

5. **Modify Student** - Update a student’s details:
   ![Modify Student](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/4f4f214b-e81b-4

ca6-b85e-1f8d393a2b48)
   ![Updated Student](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/78695dca-fc33-4c9b-bc98-06fea25673bc)

6. **Delete Student** - Remove a student’s record:
   ![Delete Student](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/72fb07b1-c7e0-42bf-b860-72cca3435121)
   ![Post Deletion](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/7a2549ca-5d9c-4fa1-ad86-bd7ce442f10e)

### 📜 Logs

For detailed logs, check the container logs:
![Logs](https://github.com/deepmancer/SE-Lab-Week9/assets/59364943/7bf57d94-f6eb-458d-8b86-bf3b80b82519)

---

### 🚀 Get Started

Clone the repository, navigate to the project directory, and launch the services using Docker Compose to experience this microservices architecture in action!

```bash
git clone https://github.com/your-repository-url.git
cd your-repository-directory
docker-compose up --build
```

---

## 📝 License

This project is licensed under the MIT License. For detailed information, please refer to the [LICENSE](LICENSE) file.

---

Feel free to explore, contribute, and provide feedback!

**Happy Coding!** 🎉
