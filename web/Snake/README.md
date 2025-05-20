# Snake

### Сложность

easy

### Информация

```

```

### Описание

змейка со скрытым условием для получения флага

### Решение

Код которой обфусцирован. Задача — получить флаг, играя в игру.

Флаг можно получить, только если змейка:

- Имеет ровно `1000` сегментов.
- Каждый сегмент имеет числовые `x` и `y` координаты.
- Змейка передаётся в функцию `validateSnakeAndRequestFlag`, которая делает POST-запрос на `/get_flag`.

Обфусцированный код содержит следующее:

- Отрисовка змейки на `canvas`.
- Логика коллизий, роста змейки, счёта и прочего.
- Функция `validateSnakeAndRequestFlag()`, которая:
  - Проверяет, что `snake.segments` — массив длины 1000 с объектами вида `{x: number, y: number}`.
  - Создаёт HMAC токен с секретом `super_secret_key` и отправляет его на сервер `/get_flag`.

```js
function isSnakeLegit(arr) {
  if (!Array.isArray(arr)) return false;
  if (arr.length !== 1000) return false;
  for (let segment of arr) {
    if (typeof segment !== 'object' || typeof segment.x !== 'number' || typeof segment.y !== 'number')
      return false;
  }
  return true;
}
```

Вместо того, чтобы играть и собирать яблоки, достаточно подменить массив сегментов на валидный и вызвать проверку вручную:


Создаём массив из 1000 валидных сегментов змейки

```js
let snakeSegments = Array.from({ length: 1000 }, (_, i) => ({ x: i % 400, y: Math.floor(i / 25) * 16 }));
```
Назначаем его как сегменты змейки

```js
snake.cells = snakeSegments;
snake.maxCells = 1000;
snake.segments = snakeSegments;
```

Вручную запускаем проверку и запрос флага

```js
validateSnakeAndRequestFlag();
```

### Флаг

goctf{sn@k3_13g1t_ch3ck}