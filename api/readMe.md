# betting API
This API service is incharge of performing CRUD operations for bet i.e creating the bets, reading the bets, updating the bets and deleting the bets.
This service requires one to have to be authenticated and the gateway service ensures that auth tokens from the authentication service has to be valif before request is sent to the betting service.

The betting service also has server, service and storage modules similar to the authentication service.
The storage service consists of interfaces to implement dependency inversion enabling choice between MySql or MongoDB database for storing betting details.

The service module contains the business logic required to perform operation to store data into the database.
This acts as the driving module in relation to the hexagonal architecture.

The server module deals with inter-service communication and we use gRPC for our communication.
We write unit tests for the service and storage modules. No tests for the server module