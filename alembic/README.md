Создание файла миграций

```
alembic revision --autogenerate -m "Yours comment"
```

---

Просмотр последней миграции

```
alembic current
```
---

Выполнение всех не применённых миграций
```
alembic upgrade head
```

---

Чтобы отменить все миграции, которые были в проекте, используется команда
```
alembic upgrade head
```

---

В Alembic есть команда history, которая позволяет увидеть в терминале все миграции в хронологическом порядке

```
alembic history
```