// Создаём массив из 1000 валидных сегментов змейки
let snakeSegments = Array.from({ length: 1000 }, (_, i) => ({ x: i % 400, y: Math.floor(i / 25) * 16 }));

// Назначаем его как сегменты змейки
snake.cells = snakeSegments;
snake.maxCells = 1000;
snake.segments = snakeSegments;

// Вручную запускаем проверку и запрос флага
validateSnakeAndRequestFlag();
