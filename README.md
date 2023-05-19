# Tutorium Backend
This repository has the codebase of Tutorium's backend part. It is implemented with FastAPI and uses RESTful APIs to transfer data. It is connected to a MySQL server to store the data. It uses to SQLAlchemy library to access the MySQL database server and apply CRUD operations on entities in ORM mode.
## How to Run
### Locally
1. Clone the repository:
   ```shell
   git clone git@github.com:TheTutorium/backend.git
1. Change the directory:
   ```shell
   cd backend
2. Install dependencies:
   ```shell
   poetry install
3. Run the code:
   ```shell
   poetry run start
4. Now you can access docs of endpoints from the following link:  
    `localhost:8000/docs`
