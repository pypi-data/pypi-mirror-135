import dis


def dis_clsdict(clsdict):
    methods = []
    attrs = []
    for func in clsdict:
        try:
            ret = dis.get_instructions(clsdict[func])
        except:
            pass
        else:
            for i in ret:
                if i.opname == 'LOAD_METHOD':
                    if i.argval not in methods:
                        methods.append(i.argval)
                if i.opname == 'LOAD_ATTR':
                    if i.argval not in attrs:
                        attrs.append(i.argval)
    return methods, attrs


def validate_method_and_attr(clsname, methods, attrs):
    if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
        raise TypeError('Некорректная инициализация сокета')
    if clsname == 'Client':
        if 'listen' in methods or 'accept' in methods:
            raise TypeError(
                'Использование методов "listen"'
                ' или "accept" недопустимо в клиентском классе')
    elif clsname == 'Server':
        if 'connect' in methods:
            raise TypeError('Использование методов "connect" '
                            'недопустимо в серверном классе')


class ClientMaker(type):

    def __init__(self, clsname, bases, clsdict):
        methods, attrs = dis_clsdict(clsdict)
        validate_method_and_attr(clsname, methods, attrs)
        super().__init__(clsname, bases, clsdict)


class ServerMaker(type):

    def __init__(self, clsname, bases, clsdict):
        methods, attrs = dis_clsdict(clsdict)
        validate_method_and_attr(clsname, methods, attrs)
        super().__init__(clsname, bases, clsdict)
