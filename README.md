# 🗺️ Opening Hours

### 📦 Dependencies

```shell
make deps
make dev-deps # dev dependencies in case you want to contribute!
```

> ❗ `Python 3.8` or above is required.

### 💻 Run Service

###### Local Run:

```shell
make run
```

###### Docker Run:

```shell
make docker-build
make docker-run
```

### 📝 Docs

###### API Specs:

API documentation can be retrieved via `http://localhost:8000/docs` along with the details of the schemas expected within the API.

###### Example HTTP Call:

```shell
curl -X POST http://localhost:8000/v1/ConvertOpeningHours -d @./test.json -H "Content-Type: application/json"
```

###### Input Format:

```json
{
  "tuesday": [
    {
      "type": "open",
      "value": 36000
    },
    {
      "type": "close",
      "value": 64800
    }
  ],
  "thursday": [
    {
      "type": "open",
      "value": 37800
    },
    {
      "type": "close",
      "value": 64800
    }
  ],
  ...
}
```

###### Output Format:

```json
Tuesday: 10 AM - 6 PM
Thursday: 10:30 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM
```

### 💄 Style Guides

```shell
make format
make lint
```

### 🚨 Tests

```shell
make test
# or
make test-with-coverage
```

### 🗣️ Discussion

- As an alternative the input format can be roughly structured as below:

```json
{
  "days": [
    {
      "name": "monday",
      "hours": [
        {
          "type": "open",
          "value": 60000
        },
        {
          "type": "close",
          "value": 64800
        }
      ]
    },
    ...
  ]
}
```

###### Pros:
- A more declarative approach to data representation with JSON.
- The representation of the above schema would facilitate the creation of the Pydantic models.
- Extensibility is improved as further fields can be easily added to each object.


###### Cons:
- The object is relatively more cumbersome and bigger in size.