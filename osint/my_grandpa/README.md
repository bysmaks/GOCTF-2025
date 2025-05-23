# Мой прадед - партизан | OSINT | Medium

### Информация

```
Я знаю, что моего прадеда звали Алексей Григорьевич, он служил в партизанских отрядах с 1941 года  
и участвовал во многих операциях, в том числе в одной из операций 1943 года, связанной с железными  
дорогами, но я точно не знаю его фамилию и название операции, в которой он участвовал.  
Необходимо найти ФИО прадеда, а также основываясь на информации об операции, в которой он участвовал,  
найти памятник, посвященной ей в районе, в котором мой прапрадед родился и участвовал в военных действиях.  
Ответом будет фамилия прадеда и координаты памятника, посвященного упомянутой операции, из района, в котором он родился.  
 
Формат флага GOCTF{}
```

### Описание

Поиск места по информации. 
мне тут нужно еще через написать для этого таска, я постараюсь завтра-послезавтра сделать

### Запуск

```sh
cd deploy
docker-compose up --build -d

```

### Выдать учаcтникам

информацию и IP:5005

### Решение
Вывод имеющейся информации:

1. Имя прадеда – Алексей; отчество – Григорьевич
2. Он был партизаном
3. Участвовал в операции на железных дорогах в 1943 году
4. Место рождения и действия как партизана совпадают
5. Неизвестны фамилия, место рождения и операция
6. Цель: найти ФИО и координаты памятника, посвящённого операции, участником которой являлся прадед, в районе, где он родился

1. Уточнение операции

Имеющаяся информация: 1943, железные дороги, партизан

Поиск:
Вбиваем в поиск:
"партизанская операция 1943 железные дороги"

Результат:
Находим информацию об операции «Рельсовая война» - крупнейшей партизанской диверсионной кампании по подрыву железных дорог в тылу врага летом 1943 года. Участвовали партизаны из Белоруссии, Украины, России.
Вывод: операция называется Рельсовая война

2. Поиск человека по имени и роли

Имеющаяся информация: Алексей, участвовал в Рельсовой войне, был партизаном; по результатам прошлого поиска знаем, какие области затрагивала операция (БССР, районы РСФСР и УССР)

Поиск в базе partizany.by, Используя фильтр: имя и отчество (Алексей Григорьевич); находим нужного человека, анализируя документы из архивов и сопоставляя их с известной информацией

Находим:
Наумчик Алексей Григорьевич, 1905 г.р., уроженец д. Хидры, Кобринский район, Брестская область https://partizany.by/partisans/77044/
ФИО найдено: Наумчик Алексей Григорьевич

3. Определение места рождения и боевых действий 

В биографии указано: родом из д. Хидры, Кобринский район; значит, искомый район для памятника – Кобринский район

4. Поиск памятника, посвящённого Рельсовой войне
Поиск по запросу:

«Памятник партизанам или Рельсовой войне в Кобрине»

Находим:
Сайт https://ikobrin.ru/kobtur-partizanam.php
На нём – памятник партизанам Кобринского района, участвовавшим в Рельсовой войне.

5. Проверка координат:
Используем ссылку на Google Maps или GPS-сервис
https://maps.app.goo.gl/UQYA2GygycarVsKo6
Получаем координаты: 52.216172, 24.397040

### Флаг

GOCTF{P@rt1zan0_pr@d33d0_28723491131}
