class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DB_TYPES = ['mariadb', 'sqlite', 'mysql']
    DB_SELECTED = ''
    DB_HOST = 'localhost'
    DB_PORT = 3306
    DB_USER = 'root'
    DB_PASSWORD = 'usuario'
    DB_NAMES = {
                'mariadb': 'student',
                'sqlite': 'student.db',
                'mysql': 'students'
                }
