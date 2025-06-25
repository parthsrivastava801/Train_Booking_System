This is an a project made in Django and Django Rest Framework to book Trains accoring to departure time and date. The webpage autoupdates every 5 seconds to provide live updates.

Hosted on ---> https://train-booking-system-zphy.onrender.com/

Instructionns to get started --->
Paste these commands in your terminal
1) git clone https://github.com/parthsrivastava801/Train_Booking_System.git
2) cd Train_Booking_System/train_booking
3) python manage.py makemigrations
4) python manage.py migrate
5) python manage.py createsuperuser (enter your username and password and go to /admin to add trains or you can do the same using API, explained later))
6) python manage.py runserver
7) to use the APIs, open POSTMAN and go to --
   /api/register/
   and enter
   {
   "username" : "your-name",
   "password" : "your-password"
   }
   and copy the Token given
   ![image](https://github.com/user-attachments/assets/766c69ae-10bc-40ad-957e-25cf2577f091)
   next time while logging in go to /api/login/ and enter
   and enter
   {
   "username" : "your-name",
   "password" : "your-password"
   }
9) open the Authorization tab and type "Authorization" in the Key and type "Token <your-token>" in Value
   ![image](https://github.com/user-attachments/assets/5b49f0ea-da10-4860-a920-4db1c357aa81)
10) Train APIs:
     GET api/trains/ – View list of available trains
    Optional query params for filtering:
    source
    destination
    departure_time (date format: YYYY-MM-DD)
    Example: /api/trains/?source=Delhi&destination=Mumbai&departure_time=2025-06-30

    GET api/trains/{id}/ – View train details (name, source, destination, timings, seats left)

    POST api/trains/ – (Admin only) Add a new train

    {
    "name": "Rajdhani Express",
    "source": "Delhi",
    "destination": "Mumbai",
    "departure_time": "2025-06-30T08:00:00Z",
    "total_seats": 50
    }


    PUT api/trains/{id}/ – (Admin only) Edit train info

    DELETE api/trains/{id}/ – (Admin only) Delete a train
    
11) Booking APIs:
    POST api/bookings/ – Book a seat on a train
    {
    "train": 3,
    "seat_number": 7
    }

    GET api/bookings/ – View your bookings

    DELETE api/bookings/{id}/ – Cancel a booking


