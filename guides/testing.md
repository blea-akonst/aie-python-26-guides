# Тесты: введение, pytest

Курс «Python и обработка данных».

## Что такое тест и зачем он нужен

Тест – маленькая программа, которая вызывает ваш код с заранее известными входными данными и сверяет результат с ожидаемым. Пройти по коду глазами и прогнать его руками можно один раз. Тест прогоняет те же проверки за доли секунды после каждой правки.

Тесты нужны, чтобы:

- поймать ошибку сразу, пока вы помните, что меняли;
- не бояться переписывать код: если сломаете старое поведение, тест упадёт;
- записать требования так, чтобы их проверяла машина. «Вещи не размножаются» из ТЗ превращается в `assert count_items(player) == before`.

Пример из lab1: дюп Валеры тестер нашёл на сервере руками. Тест из примера в конце гайда нашёл бы его ещё до выкладки. На `valera_equip.py` он падает с `assert 2 == 1`: после «надеть и снять» в инвентаре два меча.

## Как придумывать тест-кейсы

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

## pytest

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

### `assert`

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

### Сноска: что такое декоратор

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

### `@pytest.fixture`

Фикстура – функция, которая готовит данные для тестов. Тест получает её результат, если указать имя фикстуры в аргументах. Для каждого теста фикстура вызывается заново, поэтому тесты не портят друг другу данные.

```python
@pytest.fixture
def player():
    return Player("Марат", level=5)


def test_new_player_has_no_power(player):
    assert total_power(player) == 0
```

Фикстуры могут использовать другие фикстуры, как `player(sword, axe)` в примере ниже. Общие фикстуры для нескольких файлов кладут в `conftest.py`: pytest подхватывает его сам, импортировать не нужно.

### `@pytest.mark.parametrize`

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

### `pytest.raises`

Проверяет, что код выбрасывает исключение. В lab1 функции возвращают `False`, но если в пункте 4 вы решите отказывать через исключение, тест будет таким (фикстуры `player` и `axe` взяты из примера ниже):

```python
def test_full_inventory_raises(player, axe):
    player.capacity = len(player.inventory)
    with pytest.raises(ValueError, match="инвентарь"):
        equip(player, axe)
```

`match` проверяет текст сообщения регулярным выражением.

### `skip` и `xfail`

```python
@pytest.mark.skip(reason="пункт 4 ещё не сделан")
def test_full_inventory():
    ...


@pytest.mark.xfail(reason="известный дюп, чиним")
def test_valera_does_not_duplicate():
    ...
```

`skip` пропускает тест, `xfail` запускает, но ждёт падения. Оба видны в итоговом отчёте, поэтому про них не забудете, как забывают про закомментированный тест. Сдавать лабу с пропущенными тестами на основные требования не стоит.

## Пример: тесты на lab1

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
