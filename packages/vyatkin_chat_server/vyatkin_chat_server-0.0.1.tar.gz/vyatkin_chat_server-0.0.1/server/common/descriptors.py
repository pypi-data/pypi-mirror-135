import ipaddress
import sys


class ValidateAddress:
    def __set__(self, instance, value):
        try:
            if value != '':
                validate_ip_address = ipaddress.ip_address(value)
        except ValueError:
            print('Введен некорректный IP адрес')
            sys.exit(1)
        else:
            instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, name):
        self.my_attr = name


class ValidatePort:
    def __set__(self, instance, value):
        if value < 1024 or value > 65535:
            print('Необходимо использовать порт от 1024 до 65535')
            sys.exit(1)
        instance.__dict__[self.my_attr] = value

    def __set_name__(self, owner, name):
        self.my_attr = name
