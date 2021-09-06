from datetime import date
import random
import string


class FieldMaxLength:

    EMAIL = 128
    FULL_NAME = 128
    CITY = 128
    ADDRESS = 128
    LECTURE_TITLE = 128
    COURSE_NAME = 128
    SUBSCRIPTION_TYPE = 64
    CPF = 14
    CONTACT_NUMBER = 14
    RA = 9
    STATE = 2
    AUTHENTICATION_CODE = 12


class BrazilStates:

    states = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )


class IbilceCourses:

    courses = (
        ('Bio', 'Ciências Biológicas: Bacharelado/Licenciatura'),
        ('Comp', 'Ciência da Computação: Bacharelado'),
        ('Eng Alimentos', 'Engenharia de Alimentos'),
        ('Fisica', 'Física: Bacharelado em Física Biológica'),
        ('Mat', 'Matemática: Bacharelado/Licenciatura'),
        ('Quimica', 'Química: Bacharelado em Química Ambiental / Licenciatura'),
        ('Letras/Traducao', 'Letras com Habilitação de Tradutor: Bacharelado'),
        ('Letras', 'Letras: Licenciatura'),
        ('Pedagogia', 'Pedagogia: Licenciatura')
    )


class FullNameNotValidException(Exception):
    pass

#class EmailNotValidException(Exception):
    #pass


class CityNotValidException(Exception):
    pass


class AgeNotValidException(Exception):
    pass


class AddressNotValidException(Exception):
    pass


class CpfNotValidException(Exception):
    pass


class ContactNumberNotValidException(Exception):
    pass


class RaNotValidException(Exception):
    pass


def generate_validation_code():
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=FieldMaxLength.AUTHENTICATION_CODE))
    return random_code


def write_to_smtp_queue(email, code):
    with open('C:\Git repos\SEMAC-Project-Katerine\semac-smtp\emails-queue.txt', 'a') as file:
        file.write(f'{email} {code}\n')


class Validators:

    @staticmethod
    def full_name_validator(full_name):
        if full_name.count(' ') < 1:
            raise FullNameNotValidException()
        return full_name

    @staticmethod
    def age_validator(dob, expected_age):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age <= expected_age:
            raise AgeNotValidException()
        if age >= 120:  # Isso é um fix bem idiota, mas honestamente eu já estou meio cansado de fazer esse site
            raise AgeNotValidException()
        return dob

    @staticmethod
    def city_validator(city):
        if len(city) < 5:
            raise CityNotValidException()
        return city

    @staticmethod
    def address_validator(address):
        if len(address) < 5:
            raise AddressNotValidException()
        return address

    @staticmethod
    def cpf_validator(cpf):
        if len(cpf) != FieldMaxLength.CPF:
            raise CpfNotValidException()
        return cpf

    @staticmethod
    def contact_number_validator(contact_number):
        if len(contact_number) != FieldMaxLength.CONTACT_NUMBER:
            raise ContactNumberNotValidException()
        return contact_number

    @staticmethod
    def ra_validator(ra):
        if len(ra) != FieldMaxLength.RA:
            raise RaNotValidException()
        return ra
