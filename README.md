# WebServiceDevelopment

Это репозиторий, в котором будут храниться решения ДЗ по курсу
разработки веб-сервисов на питоне. Домашними заданиями является работа
над проектом. Пока что в качестве проекта сделать "датаграм" (типо
"телеграм", но "датаграм", потому что на курсе по Java нам предлагали
различать UDP и TCP так, что UDP -- это датаграмма, а TCP -- телеграмма).

## Установка необходимых пакетов
`pip install strawberry-graphql[debug-server]` -- установка библиотеки
[strawberry](https://strawberry.rocks/).
Ещё нужно установить `fastapi` и `pydantic`, позже добавлю инструкции.

## Запуск
`uvicorn main:datagram_app --reload` -- для запуска.

http://127.0.0.1:8000/docs -- ручки

http://127.0.0.1:8000/graphql -- работа с GraphQL

## GraphQL
Пример запроса:

```
{
  users (year:2001) {
    name
    additionalInfo {
      status
      birthDate  {
        year
        day
      }
    }
  }
}
```

Все схемы и типы указаны в файле `strawbery_types.py`

## Тестирование
Перед тестированием установите:
`pip install email-validator`

Запуск юнит тестов: `python -m pytest tests/unit_tests.py`

Запуск интеграционных тестов: `python -m pytest tests/integration_tests.py`