# SmileyFace
### Сложность

Easy

### Информация

```
Во время одной из операций разведчики наткнулись на странную листовку, найденную у пленного. На вид — обычная агитация, но у шифровальщиков возникло ощущение, что она несёт в себе больше, чем кажется. Документ отправили в отдел скрытых коммуникаций. Там заподозрили, что враг использует новые методы сокрытия сообщений прямо в тексте, не оставляя видимых следов. Работа закипела.
```

### Описание

Прячем данные в тексте с помощью невидимых символов Unicode Variation Selectors  
(U+E0100–U+E01EF). Если вычтесть из каждого такого символа 0xE0100, можно получить  
байты. Они добавляются после обычных символов (например, эмодзи), не меняя внешний  
вид текста. Так можно скрытно передать информацию, которую можно потом извлечь.  
После извлечения байтов делаем ROT16 и получаем флаг.  

### Выдать учаcтникам

```
😀󠄷󠄿󠄳󠅄󠄶󠅫🥰󠅓󠅢󠅩󠅠󠅤󠄠󠅏🌙󠄣󠅝󠅟󠅚󠄡󠅏💯󠅕󠅦󠅙󠄡󠅭
```

### Решение

solve/

### Флаг

GOCTF{crypt0_3moj1_evi1}
