#encoding: utf8

import os
import sys


if __name__ == '__main__':
    # 启动项目根据环境配置
    # xxxx为端口号
    # python manage.py runserver xxxx --settings=config.settings.production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exception on Python3
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and"
                "available on your PYTHONPATH evironment voiable? Did you"
                "forget to activate a virtual environmenr?"
            )
        raise
    execute_from_command_line(sys.argv)
