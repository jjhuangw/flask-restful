# REST API

## what is this?
This is a demo project using flask with SQLite database. Project contains (GET, POST, PATCH, DELETE) API functionalities. 
For further information, please check the document http://localhost:5000/apidocs/index.html

---
## install
```
pip3 install -r requirements.txt
```
Set up email configuration
- For testing, you can apply mailtrap (https://mailtrap.io/) or gmail

---
## run application in local
```
python app.py
```

---
## list all event
```
curl -X GET --header "Accept: application/json" "http://localhost:5000/events"
```

## create an new event
```
curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" -d "{
    \"end_time\": \"2020-10-31 13:30:00\",
    \"location\": \"Koganei Park\",
    \"name\": \"Mottainai Flea Market\",
    \"start_time\": \"2020-10-31 10:30:00\"
  }" "http://localhost:5000/events"
```

## update an event
```
curl -X PATCH --header "Content-Type: application/json" --header "Accept: application/json" -d "{
    \"end_time\": \"2020-11-31 13:30:00\",
    \"location\": \"Koganei Park\",
    \"name\": \"Mottainai Flea Market\",
    \"start_time\": \"2020-10-31 10:30:00\"
  }" "http://localhost:5000/events/11"
```

## remove an event
```
curl -X DELETE --header "Accept: application/json" "http://localhost:5000/events/7"
```

## sign up an event
```
curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" -d "{
  \"email\": \"dash1@gmail.com\",
  \"event_id\": 3
}" "http://localhost:5000/register"
```

## remove a participant from event
```
curl -X DELETE --header "Content-Type: application/json" --header "Accept: application/json" -d "{
  \"email\": \"dash1@gmail.com\",
  \"event_id\": 3
}" "http://localhost:5000/register"
```