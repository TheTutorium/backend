# Tutorium Backend
This repository has the codebase of Tutorium's backend part. It is implemented with FastAPI and uses RESTful APIs to transfer data. It is connected to a MySQL server to store the data. It uses to SQLAlchemy library to access the MySQL database server and apply CRUD operations on entities.
## How to Run
### Locally
0. Prerequisites:
  - You need poetry with version 1.4.2
  - You need python with version 3.10
1. Clone the repository:
   ```shell
   git clone git@github.com:TheTutorium/backend.git
2. Change the directory:
   ```shell
   cd backend
3. Create .env file with your own MySQL connection information
   ```
   DATABASE=...
   DATABASE_USERNAME=...
   HOST=...
   PASSWORD=...
4. Install dependencies:
   ```shell
   poetry install
5. Run the code:
   ```shell
   poetry run start
6. Now you can access docs of endpoints from the following link:  
    `localhost:8000/docs`
