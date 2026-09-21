This is a Flask light-controller platform with ESP32 firmware. The principal workflow is: an authenticated user sends a device command or query, Flask validates the JWT, 
the ESP32 controller dispatches to the service layer, the service resolves the user’s registered board in SQL storage, and then calls the board’s REST API.
The firmware REST server mutates or reads the in-memory device registry and GPIO-backed devices. Authentication and web-home rendering are separate product capabilities. 
The sampled files do not include the full repository implementations or firmware startup wiring.


Architecture overview
Read
This is a Flask light-controller platform with ESP32 firmware. The principal workflow is: an authenticated user sends a device command or query, Flask validates the JWT, 
the ESP32 controller dispatches to the service layer, the service resolves the user’s registered board in SQL storage, and then calls the board’s REST API. The firmware 
REST server mutates or reads the in-memory device registry and GPIO-backed devices. Authentication and web-home rendering are separate product capabilities. The sampled 
files do not include the full repository implementations or firmware startup wiring.

<img width="3996" height="6565" alt="diagram (1)" src="https://github.com/user-attachments/assets/16f6c149-388e-4e12-bb46-3d0da698f043" />
