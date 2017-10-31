# SimpleBlog

## Installation
Install dependencies:
```
$ pip install -r requirements.txt
```
Create database:
```
$ cd simpleblog
python blogapp/create_tables.py
```

Run application:
```
$ python main.py
```
## API
```
$ curl -X POST localhost:8080/users/new -d "username=Andrew";
{"success": true, "response": "User was created"}

$ curl -X POST localhost:8080/posts/new -d "user_id=1&title=hello world&text=big text&tags=first";
{"success": true, "response": "Post was created"}(simpleblog)

curl -X POST localhost:8080/posts/new -d "user_id=42&title=hello world&text=big text&tags=first"
{"success": false, "response": "User does not exists"}

$ curl -X GET localhost:8080/user/1/posts?order=asc;
{"success": true, "response": [{"author_id": 1, "title": "hello world", "id": 1, "text": "big text", "date_created": "2017-10-31T01:02:16.018670+03:00", "tags": ["first"]}]}

$ curl -X GET "localhost:8080/posts?tags=first,second&title=world&begin=2017-01-01%2000:00:00&end=2017-12-12%2023:59:59&order=asc"
{"success": true, "response": [{"author_id": 1, "title": "hello world", "id": 1, "text": "big text", "date_created": "2017-10-31T01:02:16.018670+03:00", "tags": ["first"]}]}
```
