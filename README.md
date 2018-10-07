# Покер collab

реализация клиент + сервер + GUI для игры в Texas Holdem 

## Getting Started

Collaborating in tasks here: https://trello.com/b/xWkHBM5s

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

Запустить сервер flask (по дефолу на 5000 порту)
```
...$python3 server.py
```

Пример запросов к серверу с использованием библиотеки requests
##### Логин пользователя
```
import requests

url = 'http://localhost:5000'
resp = requests.post(url + 'login', json={'login':'User1'})
print(resp.text)
```
Подробное описание api находится в файле API.txt

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Python 3.7

## Пул реквесты

Все пул реквесты должны добавляться в development branch 

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
