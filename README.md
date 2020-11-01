# REST API

## what is this?
simple api example using flask. a flask api object contains one or more functionalities (GET, POST, etc). 

API document http://localhost:5000/apidocs/index.html

## install

```
pip3 install -r requirements.txt

# Apply SMTP service, 
# e.g. mailtrap (https://mailtrap.io/) or gmail
```

## run
```
python app.py
```

## List all event
```
curl --request get http://127.0.0.1:5000/events
```

## Sign up an event
```
curl --request post --header "Content-Type: application/json" --data '{"email":"ccc@gmail.com", "event_id": 1}' http://127.0.0.1:5000/register
```

## remove from an event
```
curl --request delete --header "Content-Type: application/json" --data '{"email":"ccc@gmail.com", "event_id": 1}' http://127.0.0.1:5000/register
```