# pynosql-logger

## Installation steps if using MongoDB

```
  pip install pymongo #"pymongo[srv]" or "pymongo[aws]"
  pip install pynosql-logger
```

### Initialize
```
  from pynosql_logger.loggers import MongoLogger

  connection_string = 'your_mongodb_connection_string'
  logger = MongoLogger(connection_string)
```

## Installation steps if using ElasticSearch

```
  pip install pynosql-logger
```

### Initialize
```
  from pynosql_logger.loggers import ElasticLogger
  
  elastic_url = 'http://127.0.0.1:9200'
  logger = ElasticLogger(elastic_url)
```

### Add Log
```
  req_json = {
      'users': {
          'first_name': 'Hitesh',
          'last_name': 'Mishra',
          'email': 'hiteshmishra708@gmail.com'
      }
  }
  resp = logger.add_log(req_json)
```

### Add Bulk Log
```
  req_json = {
      'users': [{
          'first_name': 'Test',
          'last_name': 'User 1',
          'email': 'testuser1@mailnesia.com'
      }, {
          'first_name': 'Test',
          'last_name': 'User 2',
          'email': 'testuser2@mailnesia.com'
      }]
  }
  resp = logger.add_log(req_json)
```

### Get Log
```
  req_json = {
      'users': {
          'first_name': 'Hitesh'
      }
  }
  resp = logger.get_log(req_json)
```

### Add All Logs
```
  req_json = {
      'collection': 'users'
  }
  resp = logger.get_all_logs(req_json)
```