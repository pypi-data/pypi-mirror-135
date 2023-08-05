from pathlib import Path
import random


def get_files_to_render(path, patterns):
    return [
        entity
        for pattern in patterns
        for entity in path.glob(f'**/{pattern}')
        if entity.is_file()
    ]


def get_random_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.choice(chars) for _ in range(50))


def get_subdir_name(url):
    url = url.replace('https://', '').split('/')
    repo = url[2]
    branch = url[4].replace('.zip', '')
    return Path(f'{repo}-{branch}').resolve()


def is_url(template):
    template = str(template)
    schemes = ['http', 'https', 'ftp']

    if ':' not in template:
        return False

    scheme = template.split(':', 1)[0].lower()
    return scheme in schemes
