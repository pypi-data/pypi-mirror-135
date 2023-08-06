
## SingletonInjector

This simple library will instanciate singletons and inject dependencies depending on whether the parameters passed to inject where previosly marked for singleton

#### Example

1. There are two classes `Car` and `Brand`, the second one is passed the first one as a parameter. If we mark their definitions as `@injector`, we will see that the classes will still be instanciated as normal classes, but they will be injected with the singleton instanciated class.

```py
from singleton_injector import injector


@injector
class Car:
    def __init__(self):
        print("Instantiating Car class on definition")

# After defining this class marked with @injector, by itself
# should instantiate it's singleton object


@injector
class Brand:
    def __init__(self, car: Car, car2: Car):
        print("Injected Car parameters are the same: %s" % (car is car2))

```

The output for the above code should be 

```
Instantiating Car class on definition
Injected Car parameters are the same: True
```

Cheers :thumbsup: