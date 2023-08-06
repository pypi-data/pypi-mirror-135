# UsefulTools
>A simple python DSL tool

> Easy and Fast 
## How to use
1. start
```shell
cd <project path>
UsefulHelper start <project name>
UsefulHelper stop
```
2. prepare
```shell
cd <project>
python manage.py prepare
```
3. write grammar and function
```markdown
grammar.usg 
example:none
    info:info()
    things:+
        date:data()
        id:id_()
end:end()
```
```python
name = 'example'


def info():
    print('info')


def data():
    print('Data')


def id_():
    print(0)
```
4. build & create
```shell
python manage.py build
python manage.py create
```
