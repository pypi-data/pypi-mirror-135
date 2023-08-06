def say_hello(name=None):
    if name is None:
        return "hello, World!"
    else:
        return f"Hello, {name}!"