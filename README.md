# Sly parser example
Пример парсера на sly.

## Installation
```sh
python3 -m venv ENV
./ENV/bin/python3 -m pip install -r requirements.txt
./ENV/bin/python3 main.py
```

## Documentation

* [про приоритет операций и ассоциативность, если подзабыли](https://en.wikipedia.org/wiki/Order_of_operations)
* [про ассоциативность операторов](https://en.wikipedia.org/wiki/Operator_associativity)
* [про LALR(1) парсеры, если интересно](https://en.wikipedia.org/wiki/LALR_parser)
* [про BNF и EBNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)
* [про регулярные выражения раз](https://docs.python.org/3/howto/regex.html#regex-howto)
* [про регулярные выражения два](https://docs.python.org/3/library/re.html)
* [про sly раз](https://sly.readthedocs.io/en/latest/)
* [про sly два](https://github.com/dabeaz/sly)


# Grammar for visualmath.ru

Выражением являются (в порядке приоритета, у всех операторов с одинаковым
приоритетом левая ассоциативность):
* Числа (здесь нужно придумать хорошее определение записи числа)
* Константы π (`pi`, `\pi`) и e (`e`, `\e`) (кстати, давайте мы не будем
  различать маленькие и большие буквы, не только в константах а вообще везде)
* Скобки `( expr )`, `[ expr ]`, `{ expr }`
* Унарный минус `- expr` и унарный плюс `+ expr`
* Степень `expr ^ expr`
* Функции `sin`, `cos`, `tg`, `ctg`, также их арк-функции (`arcsin`, ...) и с
  backslash'ем в начале (`\sin`, `\arcsin`, ...). Функции записываются как
  `sin expr`.  Функция `exp`, записывается как `exp expr`. Функция `log` от
  одного аргумента (аргумент - то что логарифмируем, основание натуральное),
  записывается как `log expr` или `ln expr`. Функция `log` от двух аргументов
  (первый аргумент - основание, второй - то что логарифмируем) записывается
  как `log(expr, expr)` или `ln(expr, expr)`.
* Умножение `expr * expr` и деление `expr / expr`
* Сложение `expr + expr` и вычитание `expr - expr`
