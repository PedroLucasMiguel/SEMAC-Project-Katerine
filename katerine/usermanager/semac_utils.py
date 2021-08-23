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