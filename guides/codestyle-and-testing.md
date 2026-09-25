# Кодстайл и тесты: шпаргалка к лабам

Курс «Python и обработка данных». Здесь то, что проверяют автотесты на каждый push: flake8 смотрит на оформление, pytest гоняет ваши тесты. Половина баллов за лабу приходит именно отсюда.

---

## Часть 1. Кодстайл

### Что это и зачем

Кодстайл – договорённость, как оформлять код: где ставить пробелы, как называть переменные, какой длины строки. Интерпретатору всё равно, он выполнит и `x=1`, и `x = 1`. Разница видна человеку, который читает.

А читают код намного чаще, чем пишут. Ваш код прочтут преподаватель на защите, одногруппник на код-ревью и вы сами через месяц, когда забудете, что там происходило. Если у всех одинаковое оформление, глаз не спотыкается о пробелы и скобки и сразу видит логику. Если у каждого своё, первые пять минут уходят на привыкание.

В Python такая договорённость записана в документ [PEP 8](https://peps.python.org/pep-0008/). PEP (Python Enhancement Proposal) – это документы, через которые развивается язык, а восьмой из них целиком про стиль. Им пользуется почти всё сообщество, поэтому код из чужой библиотеки на GitHub выглядит так же, как ваш.

Есть и практичная причина: на работе код с кривым оформлением просто не примут в общую ветку. Линтер в CI упадёт раньше, чем до кода дойдёт живой ревьюер.

### Главные правила PEP 8

Ниже самые частые нарушения. Коды в скобках (E225, E231...) – то, что выведет flake8; по ним удобно искать ошибку в выводе. Список собран по реальным сдачам lab1: на группу из 25 человек flake8 нашёл 173 нарушения E231, 121 – E225 и 92 – E501.

#### Отступы: 4 пробела (E111)

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

#### Пробелы вокруг операторов и после запятых (E225, E231)

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

#### Длина строки: до 79 символов (E501)

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

#### Пустые строки (E302, E303, W391)

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

#### Лишние пробелы в конце строк (W291, W293)

Пробелы после последнего символа строки и пробелы в «пустой» строке не видны глазом, но flake8 их видит. Включите в редакторе отображение пробелов или автоудаление при сохранении (в VS Code это настройка `files.trimTrailingWhitespace`).

#### Сравнение с None, True и False (E711, E712)

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

#### Импорты (F401, F403, F405, E401)

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

#### Имена

| Что | Стиль | Пример |
|---|---|---|
| переменные, функции, модули | `snake_case` | `total_power`, `test_equipment.py` |
| классы | `CapWords` | `Item`, `Player` |
| константы | `UPPER_CASE` | `SLOTS`, `HANDS` |

Имя объясняет, что лежит в переменной: `old_item` вместо `x`, `count_items` вместо `f`. Однобуквенные имена оставьте для счётчиков в коротких циклах. `l`, `O` и `I` не используйте никогда: в некоторых шрифтах их не отличить от `1` и `0`.

#### Комментарии (E261, E262, E265)

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

### flake8

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

#### autopep8

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

#### black

black – форматтер, который принят во многих командах. Настроек у него почти нет, зато весь код после него выглядит одинаково.

```bash
python -m pip install black
black --check --diff equipment.py
black equipment.py
black .
```

`--check --diff` показывает правки, не меняя файл. Без флагов black переписывает файлы сразу.

У black есть две особенности, о которых стоит знать заранее. Он переносит строки по длине 88 символов, а не 79, поэтому flake8 после него всё равно найдёт E501. Лечится это запуском `black -l 79 .` или строкой `max-line-length = 88` в `.flake8`. Кроме того, black меняет только оформление: `import os, sys`, `== None` и `== True` из примера выше он оставит как есть.

#### В редакторе

В VS Code поставьте расширение autopep8 или Black Formatter от Microsoft, потом вызовите Format Document (Shift+Alt+F, на macOS Shift+Option+F). Чтобы форматирование срабатывало при каждом сохранении, включите настройку `editor.formatOnSave`. В PyCharm отдельно ничего ставить не нужно: Code → Reformat Code (Ctrl+Alt+L, на macOS Option+Command+L).

После любого форматтера всё равно запустите flake8. Ошибки вроде F401 и F841 за вас никто не исправит: за ними обычно стоит забытый или лишний кусок логики.

---

## Часть 2. Тестирование

### Что такое тест и зачем он нужен

Тест – маленькая программа, которая вызывает ваш код с заранее известными входными данными и сверяет результат с ожидаемым. Пройти по коду глазами и прогнать его руками можно один раз. Тест прогоняет те же проверки за доли секунды после каждой правки.

Тесты нужны, чтобы:

- поймать ошибку сразу, пока вы помните, что меняли;
- не бояться переписывать код: если сломаете старое поведение, тест упадёт;
- записать требования так, чтобы их проверяла машина. «Вещи не размножаются» из ТЗ превращается в `assert count_items(player) == before`.

Пример из lab1: дюп Валеры тестер нашёл на сервере руками. Тест из примера в конце этой части нашёл бы его ещё до выкладки. На `valera_equip.py` он падает с `assert 2 == 1`: после «надеть и снять» в инвентаре два меча.

### Как придумывать тест-кейсы

Тест-кейс – одна ситуация из трёх частей: исходное состояние, действие, ожидаемый результат. Эту схему называют Arrange – Act – Assert (подготовка – действие – проверка), и в хорошем тесте три части видны сразу.

Откуда брать кейсы:

1. Из ТЗ. Каждое правило – минимум один тест. «Если слот занят, прежняя вещь возвращается в инвентарь» – готовый тест.
2. Из инвариантов. Инвариант – то, что должно оставаться верным после любой операции. В lab1 это количество вещей у игрока. Проверяйте его в каждом тесте, где вещи двигаются, в том числе там, где операция не состоялась.
3. Из границ. Уровень 9 при требовании 10 и уровень ровно 10, прочность 0, пустой слот, полный инвентарь. Ошибки чаще всего сидят в `<` вместо `<=`.
4. Из «плохих» входов. Вещи нет в инвентаре, снимаем из пустого слота.

Правила для тестовых функций:

- имя начинается с `test_` и говорит, что проверяется: `test_two_handed_frees_both_hands`, а не `test_3`;
- один тест проверяет одно поведение. Несколько `assert` допустимы, если все они про одно действие;
- тесты не зависят друг от друга и от порядка запуска. Каждый создаёт свои объекты сам (или через фикстуру, см. ниже);
- тест сначала должен упасть. Если он зелёный на заведомо сломанном коде (например, на `valera_equip.py`), он ничего не проверяет.

### pytest

pytest – самый распространённый фреймворк для тестов в Python. Тесты в нём – обычные функции с обычным `assert`, а при падении pytest показывает, какие значения были слева и справа.

Установка:

```bash
python -m pip install pytest
```

Запуск:

```bash
pytest
pytest -v
pytest test_equipment.py
pytest test_equipment.py::test_two_handed_frees_both_hands
pytest -k "two_handed or broken"
pytest -x
```

По порядку: все тесты в папке, подробный вывод по каждому тесту, один файл, один тест, тесты с подходящими словами в имени, остановка на первом упавшем.

pytest сам находит файлы `test_*.py` (или `*_test.py`) и в них функции, имя которых начинается с `test_`. Если функция называется `check_equip`, она не запустится, и pytest честно напишет `no tests ran`. Это тоже «ноль упавших тестов», но ничего не проверено.

Упавший тест выглядит так:

```
    def test_equip_unequip_does_not_duplicate(player, sword):
        before = count_items(player)
        equip(player, sword)
        unequip(player, "right_hand")
        assert count_items(player) == before
>       assert player.inventory.count(sword) == 1
E       assert 2 == 1
```

Стрелка `>` показывает строку, где упало, а `E` – что с чем сравнивалось.

#### `assert`

Основной инструмент. После `assert` пишется выражение, которое должно быть истинным:

```python
assert equip(player, sword) is True
assert sword in player.inventory
assert total_power(player) == 25
assert len(player.inventory) <= player.capacity
```

Дробные числа точно сравнивать нельзя, `0.1 + 0.2 == 0.3` даёт `False`. Для них есть `pytest.approx`:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
```

#### Сноска: что такое декоратор

Дальше в примерах перед функциями стоят строки вида `@pytest.fixture`. Символ `@` с именем над `def` называется декоратором. Декоратор меняет функцию или сообщает про неё что-то дополнительное, не трогая её код.

Технически декоратор – обычная функция, которая принимает функцию и возвращает функцию. Вот декоратор, который переводит результат в верхний регистр:

```python
def loud(func):
    def wrapper(name):
        return func(name).upper()
    return wrapper


@loud
def greet(name):
    return f"привет, {name}"


print(greet("марат"))
```

Выведет `ПРИВЕТ, МАРАТ`. Запись `@loud` над `def greet` – сокращение для такой строки после определения функции:

```python
greet = loud(greet)
```

Python передаёт `greet` в `loud` и под тем же именем сохраняет то, что вернулось, то есть `wrapper`.

Декоратор может и не оборачивать функцию, а просто повесить на неё метку и вернуть её же:

```python
def slow(func):
    func.is_slow = True
    return func


@slow
def test_big_inventory():
    assert True
```

Декораторы pytest в основном работают так же. `@pytest.fixture` помечает функцию как фикстуру, `@pytest.mark.skip` – как тест, который надо пропустить. Потом pytest собирает тесты, видит метки и решает, что с какой функцией делать. Когда у декоратора есть скобки, как в `@pytest.mark.parametrize(...)`, сначала выполняется вызов в скобках. Он возвращает декоратор, и уже этот декоратор применяется к функции.

Самим писать декораторы в курсе пока не нужно, для тестов хватит готовых.

#### `@pytest.fixture`

Фикстура – функция, которая готовит данные для тестов. Тест получает её результат, если указать имя фикстуры в аргументах. Для каждого теста фикстура вызывается заново, поэтому тесты не портят друг другу данные.

```python
@pytest.fixture
def player():
    return Player("Марат", level=5)


def test_new_player_has_no_power(player):
    assert total_power(player) == 0
```

Фикстуры могут использовать другие фикстуры, как `player(sword, axe)` в примере ниже. Общие фикстуры для нескольких файлов кладут в `conftest.py`: pytest подхватывает его сам, импортировать не нужно.

#### `@pytest.mark.parametrize`

Один тест на много наборов данных. Удобно для граничных значений:

```python
@pytest.mark.parametrize(
    "durability, expected_power",
    [(100, 10), (1, 10), (0, 0)],
    ids=["целая", "почти сломана", "сломана"],
)
def test_power_depends_on_durability(durability, expected_power):
    ring = Item("Кольцо", "ring_1", power=10, durability=durability)
    player = Player("Игрок", inventory=[ring])
    equip(player, ring)

    assert total_power(player) == expected_power
```

pytest запустит три отдельных теста, а `ids` задаёт им понятные имена в выводе.

#### `pytest.raises`

Проверяет, что код выбрасывает исключение. В lab1 функции возвращают `False`, но если в пункте 4 вы решите отказывать через исключение, тест будет таким (фикстуры `player` и `axe` взяты из примера ниже):

```python
def test_full_inventory_raises(player, axe):
    player.capacity = len(player.inventory)
    with pytest.raises(ValueError, match="инвентарь"):
        equip(player, axe)
```

`match` проверяет текст сообщения регулярным выражением.

#### `skip` и `xfail`

```python
@pytest.mark.skip(reason="пункт 4 ещё не сделан")
def test_full_inventory():
    ...


@pytest.mark.xfail(reason="известный дюп, чиним")
def test_valera_does_not_duplicate():
    ...
```

`skip` пропускает тест, `xfail` запускает, но ждёт падения. Оба видны в итоговом отчёте, поэтому про них не забудете, как забывают про закомментированный тест. Сдавать лабу с пропущенными тестами на основные требования не стоит.

### Пример: тесты на lab1

Файл `test_equipment.py` лежит рядом с `equipment.py`. Это пример, а не полный набор: пункт 4 (полный инвентарь) зависит от выбранного вами варианта, и тест на него придётся написать самостоятельно.

```python title=test_equipment.py
import pytest

from equipment import Item, Player, equip, unequip, total_power


def count_items(player):
    unique = []
    for item in player.inventory + list(player.slots.values()):
        if item is not None and all(item is not seen for seen in unique):
            unique.append(item)
    return len(unique)


@pytest.fixture
def sword():
    return Item("Меч", "right_hand", power=10)


@pytest.fixture
def axe():
    return Item("Секира", "right_hand", power=25, two_handed=True)


@pytest.fixture
def player(sword, axe):
    return Player("Марат", level=5, inventory=[sword, axe])


def test_equip_moves_item_from_inventory_to_slot(player, sword):
    assert equip(player, sword) is True
    assert player.slots["right_hand"] is sword
    assert sword not in player.inventory


def test_equip_into_busy_slot_returns_old_item(player, sword):
    dagger = Item("Кинжал", "right_hand", power=4)
    player.inventory.append(dagger)
    before = count_items(player)

    equip(player, sword)
    equip(player, dagger)

    assert player.slots["right_hand"] is dagger
    assert sword in player.inventory
    assert count_items(player) == before


def test_equip_unequip_does_not_duplicate(player, sword):
    before = count_items(player)

    equip(player, sword)
    unequip(player, "right_hand")

    assert count_items(player) == before
    assert player.inventory.count(sword) == 1


def test_two_handed_frees_both_hands(player, sword, axe):
    shield = Item("Щит", "left_hand", power=3)
    player.inventory.append(shield)
    equip(player, sword)
    equip(player, shield)
    before = count_items(player)

    assert equip(player, axe) is True

    assert sword in player.inventory
    assert shield in player.inventory
    assert total_power(player) == 25
    assert count_items(player) == before


@pytest.mark.parametrize(
    "level, expected",
    [(1, False), (9, False), (10, True), (42, True)],
)
def test_level_requirement(level, expected):
    crown = Item("Корона", "head", level_req=10)
    player = Player("Игрок", level=level, inventory=[crown])
    before = count_items(player)

    assert equip(player, crown) is expected
    assert count_items(player) == before


def test_broken_item_still_occupies_slot(player):
    helmet = Item("Шлем", "head", power=7, durability=0)
    player.inventory.append(helmet)
    equip(player, helmet)

    assert player.slots["head"] is helmet
    assert total_power(player) == 0
    assert unequip(player, "head") is True
    assert helmet in player.inventory


def test_unequip_empty_slot(player):
    before = count_items(player)

    assert unequip(player, "head") is False
    assert count_items(player) == before
```

На что обратить внимание:

- `count_items` считает уникальные вещи через `is`, а не через `==` или `in`. Двуручная секира может лежать в обоих слотах рук одним объектом, и считать её дважды нельзя. А `in` и `==` сравнивают значения, а не объекты, поэтому две разные одинаковые вещи для них неразличимы.
- `test_equip_unequip_does_not_duplicate` проверяет ровно тот сценарий из тикета: надел, снял, мечей должно остаться столько же.
- `test_broken_item_still_occupies_slot` ловит ошибку из пункта 3: если реализация проверяет слот через `if player.slots[slot]:`, сломанный шлем не снимется.
- `before` фиксируется после подготовки, но до действия, иначе инвариант сравнивается не с тем состоянием.

---

## Перед push

```bash
flake8 .
pytest -v
```

Оба должны пройти чисто. Тогда в Actions тоже будет зелёно, и на защите разговор пойдёт о решении, а не о пробелах.
