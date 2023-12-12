class trace(object):
    def __init__(self, func):
        self.func = func

        try:
            self.name = func.__name__
        except AttributeError:
            self.name = f'<anonymous function {id(func)}>'

        self.active_calls = 0

    def __call__(self, *args, **kw):
        call = [repr(arg) for arg in args]

        for (k, v) in kw.items():
            call.append(f'{k} = {v!r}')

        nesting = self.active_calls * " "
        print(f'{nesting}{self.name}({", ".join(call)})')

        self.active_calls += 1
        res = self.func(*args, **kw)
        self.active_calls -= 1
        
        print(f'{nesting}=> {res!r}')

        return res

@trace
def fact(n):
    if n <= 0: return 1

    return n * fact(n-1)

def trace2(func):
    name = getattr(func, '__name__', f'<anonymous function {id(func)}>')

    active_calls = [0]

    def inner(*args, **kw):
        call = [repr(arg) for arg in args]

        for (k, v) in kw.items():
            call.append(f'{k} = {v!r}')

        nesting = active_calls[0] * " "
        print(f'{nesting}{name}({", ".join(call)})')

        active_calls[0] += 1
        res = func(*args, **kw)
        active_calls[0] -= 1
        
        print(f'{nesting}=> {res!r}')

        return res

    try:
        inner.__name__ = func.__name__
    except AttributeError:
        pass

    return inner

@trace2
def fact2(n):
    if n <= 0: return 1

    return n * fact2(n-1)

@trace
@trace2
def fact3(n):
    if n <= 0: return 1

    return n * fact3(n-1)
