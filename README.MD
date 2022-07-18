# JumpingMinds Demo

## Overview :-
Elevator Problem.


## INSTALLATION :-
1. Clone the repo in your local system.

2. Create a virtual environment.
    - MAC users :-
        Refer to :- https://gist.github.com/pandafulmanda/730a9355e088a9970b18275cb9eadef3

    - Windows and Linux users :-
        Refer to :- https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/

3. Install Requirements
    Change directory to the root folder and run
    
    `pip install -r requirements.txt` 

4. Connect POSTGRES DB. Change settings (hostname, db_name, port) as per your configs.

5. Make migrations and migrate.
    Run these commands

    `python manage.py makemigrations` and `python manage.py migrate`

6. Start the server.

    `python manage.py runserver`

7. You are good to go. Happy hacking !


## API Description :- 
1. Add Elevators :- http://127.0.0.1:8000/add_elevators

2. Fetch Next Destination :- http://127.0.0.1:8000/fetch_next_destination?elevator_id=5

3. Fetch Direction :- http://127.0.0.1:8000/fetch_direction?elevator_id=1

4. Fetch All Requests :- http://127.0.0.1:8000/fetch_all_requests?elevator_id=2

5. Mark Elevator Down :- http://127.0.0.1:8000/mark_elevator_down?elevator_id=6

6. Call Elevator :- http://127.0.0.1:8000/call_elevator

7. Open or Close Door :- http://127.0.0.1:8000/open_or_close_door

Note :- The details on each request can be found in the postman collection file ( -> JumpingMinds.postman_collection.json )