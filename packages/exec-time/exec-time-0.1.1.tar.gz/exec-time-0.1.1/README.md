# exec-time
A code snippet used to compare execution time of two Python code

### Docs to use
 - Add your code snippets in `first_func` and `second_func` respectively for comparison
```python
# === USAGE ===
@exec_time
def first_func():
    '''Here goes function 1'''
    x = 0
    for i in range(1, 10001):
        x += 10

@exec_time
def second_func():
    '''Here goes function 2'''
    x = 0
    for i in range(1, 101):
        x += 10

first_func()
second_func()
```

```
# === OUTPUT ===
first_func function executed in : 0.32839999767020345 mil sec
second_func function executed in : 0.006199989002197981 mil sec
```
 - That's it, enjoy 🍷
