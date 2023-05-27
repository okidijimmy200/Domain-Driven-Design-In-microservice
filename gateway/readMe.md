The API gateway service is incharge of directing traffic to the respective services depending on the activity to be performed.
We do use the hexagonal architecture to break down this service into the 
1. Driving
2. Server
3. Driven

To implement this architecture, one needs to understand SOLID principles which is a concept I cover in one of the projects above and also written an article. Check it out here.
medium.com/@okidijimmy/mastering-clean-code-harnessing-the-power-of-solid-principles-in-python-development-f7a09efa159d.

The driving section ie Service is the responsible for steering the application.
The service consists of the api, auth and registration with an interface which acts as a handshake/contract to the different implementations.

The driven section i.e provider is what is being controlled. This module handles inter-service communications in this case we use gRPC for our communication to the other services

The Server since this being the gateway consists of Flask server with routes connection to the outside world.

The main.py file the file we run that contains the different modules injected so here we have the driven being injected into the driving module.

We do perform tests for the server only in the gateway service.

This architecture is very good for very large scale applications and managing increasing complexities