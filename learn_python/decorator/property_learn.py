# coding:utf-8

class decorator_learn:

    def __init__(self, name = None):
        if name is not None:
            self._name = name


    def _get_name(self):
        return self._name

    def _set_name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError('%s name must be str, got %s:' % (type(self).__name__,
                type(name).__name__))

    name = property(_get_name, _set_name)

if __name__ == "__main__":
    propertytest = decorator_learn("zhqs");
    print "get:", propertytest.name;
    propertytest.name = "decorator_learn"
    print "after set:", propertytest.name