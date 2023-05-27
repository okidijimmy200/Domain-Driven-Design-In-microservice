Here we use Domain Driven Design  to decompose a sports betting application into three microservices
a. Auth Service which is incharge user registration, authentication and authorization
b. Gateway Service which is incharge of handling incoming traffic from the frontend. We use Flask as our server 
c. API Service which is incharge of performing CRUD operations with bets. We ensure that user is authenticated and authorized to perform CRUD operations
We use gRPC as our inter-service communication platform.

Each of the Services has their respective readMe explainin into detail their operation and structural breakdown.