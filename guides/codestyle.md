# Кодстайл: PEP8 и flake8

Курс «Python и обработка данных».

## Что это и зачем

Кодстайл – договорённость, как оформлять код: где ставить пробелы, как называть переменные, какой длины строки. Интерпретатору всё равно, он выполнит и `x=1`, и `x = 1`. Разница видна человеку, который читает.

А читают код намного чаще, чем пишут. Ваш код прочтут преподаватель на защите, одногруппник на код-ревью и вы сами через месяц, когда забудете, что там происходило. Если у всех одинаковое оформление, глаз не спотыкается о пробелы и скобки и сразу видит логику. Если у каждого своё, первые пять минут уходят на привыкание.

В Python такая договорённость записана в документ [PEP 8](https://peps.python.org/pep-0008/). PEP (Python Enhancement Proposal) – это документы, через которые развивается язык, а восьмой из них целиком про стиль. Им пользуется почти всё сообщество, поэтому код из чужой библиотеки на GitHub выглядит так же, как ваш.

Есть и практичная причина: на работе код с кривым оформлением просто не примут в общую ветку. Линтер в CI упадёт раньше, чем до кода дойдёт живой ревьюер.

## Главные правила PEP 8

Ниже самые частые нарушения. Коды в скобках (E225, E231...) – то, что выведет flake8; по ним удобно искать ошибку в выводе. Список собран по реальным сдачам lab1: на группу из 25 человек flake8 нашёл 173 нарушения E231, 121 – E225 и 92 – E501.

### Отступы: 4 пробела (E111)

Не табы, не 2 пробела. Любой редактор можно настроить так, чтобы Tab вставлял 4 пробела.

Плохо:

```python
def total(items):
  s = 0
  for item in items:
      s += item
  return s
```

Хорошо:

```python
def total(items):
    s = 0
    for item in items:
        s += item
    return s
```

### Пробелы вокруг операторов и после запятых (E225, E231)

Бинарные операторы (`=`, `==`, `+`, `<` и т. д.) окружаются пробелами. После запятой и двоеточия в словаре ставится пробел, перед ними – нет.

Плохо:

```python
power=item.power*2
if level>=10:
    slots={"head":None,"body":None}
    equip(player,item)
```

Хорошо:

```python
power = item.power * 2
if level >= 10:
    slots = {"head": None, "body": None}
    equip(player, item)
```

Исключение: у аргументов со значением по умолчанию и у именованных аргументов пробелов вокруг `=` нет (E251).

```python
def make_item(name, power=0, durability=100):
    return Item(name, "head", power=power, durability=durability)
```

### Длина строки: до 79 символов (E501)

Длинную строку переносите внутри скобок: Python сам понимает, что выражение продолжается.

Плохо:

```python
sword = Item("Меч короля", "right_hand", power=50, durability=100, level_req=20, two_handed=False)
```

Хорошо:

```python
sword = Item("Меч короля", "right_hand", power=50, durability=100,
             level_req=20, two_handed=False)

sword = Item(
    "Меч короля",
    "right_hand",
    power=50,
    level_req=20,
)
```

Обратный слеш `\` для переноса тоже работает, но PEP 8 советует скобки.

### Пустые строки (E302, E303, W391)

Между функциями и классами верхнего уровня – две пустые строки. Между методами внутри класса – одна. Больше двух пустых строк подряд быть не должно, а в конце файла ровно один перевод строки.

Плохо:

```python
import pytest
def test_one():
    assert 1 + 1 == 2
def test_two():
    assert 2 * 2 == 4
```

Хорошо:

```python
import pytest


def test_one():
    assert 1 + 1 == 2


def test_two():
    assert 2 * 2 == 4
```

### Лишние пробелы в конце строк (W291, W293)

Пробелы после последнего символа строки и пробелы в «пустой» строке не видны глазом, но flake8 их видит. Включите в редакторе отображение пробелов или автоудаление при сохранении (в VS Code это настройка `files.trimTrailingWhitespace`).

### Сравнение с None, True и False (E711, E712)

С `None` сравнивают через `is` / `is not`. С `True` и `False` не сравнивают вообще.

Плохо:

```python
if player.slots["head"] == None:
    ...
if item.two_handed == True:
    ...
```

Хорошо:

```python
if player.slots["head"] is None:
    ...
if item.two_handed:
    ...
```

В lab1 от этого зависит правильность решения. `if player.slots[slot]:` вызывает у вещи `__bool__`, и сломанный шлем с прочностью 0 превращается в `False`, как будто слот пуст. Проверка `is None` смотрит, лежит ли в слоте хоть что-то, и на такое не попадается (это пункт 3 задания).

### Импорты (F401, F403, F405, E401)

Импорты стоят в начале файла, по одному модулю на строку. Сначала стандартная библиотека, потом сторонние пакеты, потом свои модули, группы разделяются пустой строкой. Импорт со звёздочкой не используем: непонятно, откуда взялось имя, и flake8 ругается на каждое его использование (F405 у группы встретился 90 раз).

Плохо:

```python
import os, sys
from equipment import *
```

Хорошо:

```python
import os
import sys

import pytest

from equipment import Item, Player, equip, unequip
```

Импортировали и не использовали – F401. Такой импорт просто удалите.

### Имена

| Что | Стиль | Пример |
|---|---|---|
| переменные, функции, модули | `snake_case` | `total_power`, `test_equipment.py` |
| классы | `CapWords` | `Item`, `Player` |
| константы | `UPPER_CASE` | `SLOTS`, `HANDS` |

Имя объясняет, что лежит в переменной: `old_item` вместо `x`, `count_items` вместо `f`. Однобуквенные имена оставьте для счётчиков в коротких циклах. `l`, `O` и `I` не используйте никогда: в некоторых шрифтах их не отличить от `1` и `0`.

### Комментарии (E261, E262, E265)

После `#` ставится пробел, перед комментарием в конце строки – два пробела.

Плохо:

```python
#вернуть старую вещь
inventory.append(old)#в инвентарь
```

Хорошо:

```python
# вернуть старую вещь
inventory.append(old)  # в инвентарь
```

Переменная, которой присвоили значение и больше не использовали (F841), обычно значит забытый кусок логики. Посмотрите на неё внимательнее, прежде чем удалять.

## flake8

flake8 – линтер: он читает код, ничего не запуская, и сообщает о нарушениях PEP 8, а также о неиспользуемых импортах, необъявленных именах и похожих ошибках. Это его проверка работает в Actions на каждый push.

Установка (лучше в виртуальное окружение проекта):

```bash
python -m pip install flake8
```

Проверка всей папки или одного файла:

```bash
flake8 .
flake8 equipment.py
```

Каждая строка вывода – одно нарушение в формате `файл:строка:колонка: код описание`:

```
./equipment.py:50:1: W293 blank line contains whitespace
./equipment.py:61:17: E225 missing whitespace around operator
./test_equipment.py:1:1: F403 'from equipment import *' used; unable to detect undefined names
```

Пустой вывод значит, что всё чисто.

Полезные опции:

```bash
flake8 --statistics --count .
flake8 --select=E225,E231 .
flake8 --extend-ignore=E501 .
flake8 --max-line-length=100 .
```

Первая считает, сколько раз встретилась каждая ошибка, вторая показывает только выбранные коды, третья скрывает выбранные коды, четвёртая меняет лимит длины строки.

Чтобы не писать опции каждый раз, их кладут в файл `.flake8` (или `setup.cfg`, `tox.ini`) в корне проекта:

```ini title=.flake8
[flake8]
max-line-length = 79
exclude = .git, __pycache__, .venv
```

Если одну конкретную строку нужно пропустить, в её конец дописывают `# noqa: E501` с кодом ошибки. Пользуйтесь этим редко и с понятной причиной: на защите спросят.

**Большую часть ошибок оформления можно исправить автоматически.** Это делают форматтеры: они сами расставляют пробелы, пустые строки и переносы, а логику кода не трогают. Самые известные – `autopep8` и `black`.

### autopep8

autopep8 исправляет ровно то, на что ругается flake8, и держится тех же 79 символов. Для учебных лаб это самый удобный вариант.

```bash
python -m pip install autopep8
autopep8 --diff equipment.py
autopep8 --in-place equipment.py
autopep8 --in-place --aggressive --aggressive equipment.py
autopep8 --in-place --recursive .
```

`--diff` только показывает, что поменяется, а сам файл не трогает. `--in-place` переписывает файл, без этого флага autopep8 просто напечатает исправленный код в терминал. Двойной `--aggressive` разрешает правки посерьёзнее: `== None` превращается в `is None`, а `== True` пропадает совсем. `--recursive .` проходит по всем файлам в папке.

Возьмём такой файл, на который flake8 выдаёт девять замечаний:

До:

```python
import os, sys
def equip(player,item):
    if player.level<item.level_req or item.two_handed == True:
        return False
    if player.slots[item.slot] != None:
        player.inventory.append(player.slots[item.slot])
    player.slots[item.slot]=item
    player.inventory.remove(item)
    return True
```

После `autopep8 --in-place --aggressive --aggressive equipment.py`:

```python
import os
import sys


def equip(player, item):
    if player.level < item.level_req or item.two_handed:
        return False
    if player.slots[item.slot] is not None:
        player.inventory.append(player.slots[item.slot])
    player.slots[item.slot] = item
    player.inventory.remove(item)
    return True
```

flake8 после этого выдаст только две строки:

```
./equipment.py:1:1: F401 'os' imported but unused
./equipment.py:2:1: F401 'sys' imported but unused
```

Лишние импорты autopep8 удалять не стал: он не знает, нужны они вам или нет. Это решаете вы.

С `--aggressive` сначала смотрите `--diff`. `if x == True` и `if x` совпадают, только когда в `x` лежит `True` или `False`. Если там строка или число, поведение изменится.

### black

black – форматтер, который принят во многих командах. Настроек у него почти нет, зато весь код после него выглядит одинаково.

```bash
python -m pip install black
black --check --diff equipment.py
black equipment.py
black .
```

`--check --diff` показывает правки, не меняя файл. Без флагов black переписывает файлы сразу.

У black есть две особенности, о которых стоит знать заранее. Он переносит строки по длине 88 символов, а не 79, поэтому flake8 после него всё равно найдёт E501. Лечится это запуском `black -l 79 .` или строкой `max-line-length = 88` в `.flake8`. Кроме того, black меняет только оформление: `import os, sys`, `== None` и `== True` из примера выше он оставит как есть.

### В редакторе

В VS Code поставьте расширение autopep8 или Black Formatter от Microsoft, потом вызовите Format Document (Shift+Alt+F, на macOS Shift+Option+F). Чтобы форматирование срабатывало при каждом сохранении, включите настройку `editor.formatOnSave`. В PyCharm отдельно ничего ставить не нужно: Code → Reformat Code (Ctrl+Alt+L, на macOS Option+Command+L).

После любого форматтера всё равно запустите flake8. Ошибки вроде F401 и F841 за вас никто не исправит: за ними обычно стоит забытый или лишний кусок логики.
