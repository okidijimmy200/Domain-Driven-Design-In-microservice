# Auth Service
This service in incharge of handling user registration, authentication and authorization.

We do use dependency inversion principle to create connections to either a Mysql or Mongodb.

The application is broken down into the server, storage and service modules using the hexagonal architecute.

The storage module contains interfaces and is handles logic for the different interactions with the respective databases.

The Service module also made of interfaces and classes that handle business logic that deals with user registration, authentication or authorization. For example in the registration, we do have the hash password operation before storing to database.

The server in the auth service handles inter-service communication. Here we use gRPC for communication because its faster and lighter. We perform unit tests for service and the storage modules. No tests for the server.