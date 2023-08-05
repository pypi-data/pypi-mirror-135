import os
import shutil
from urllib.request import urlretrieve
from zipfile import is_zipfile
from zipfile import ZipFile

from jinja2 import Template

from .utils import get_files_to_render
from .utils import get_subdir_name
from .utils import is_url


def handle_template(
    project_name,
    target,
    template,
    files_patterns,
    context
):
    if is_url(template):
        handle_url(template, target, project_name)
    elif is_zipfile(template):
        handle_zip(template, target, project_name)
    else:
        handle_tree(template, target, project_name)

    for file in get_files_to_render(target, files_patterns):
        content = Template(file.read_text()).render(**context)
        eof = '\n' if file.stat().st_size > 0 else ''
        file.write_text(content + eof)


def handle_tree(
    path,
    target,
    project_name,
):
    os.makedirs(target, exist_ok=True)

    for srcentry in path.iterdir():
        dst = target / srcentry.name

        if srcentry.is_file():
            if srcentry.match('*-tpl'):
                dst = dst.with_name(dst.name.replace('-tpl', ''))
            shutil.copyfile(srcentry, dst)
        if srcentry.is_dir():
            if srcentry.match('project_name'):
                dst = dst.with_name(project_name)
            handle_tree(srcentry, dst, project_name)


def handle_url(url, target, project_name):
    content, _ = urlretrieve(url)

    with ZipFile(content) as archive:
        archive.extractall()

    # There is subdir in the GitHub repository zip archive
    # like this: django-start-tool-main -- '{repo_name}-{branch_name}'.
    # It is necessary to extract all the contents and delete this subdir.
    subdir_name = get_subdir_name(url)
    handle_tree(subdir_name, target, project_name)
    shutil.rmtree(subdir_name)


def handle_zip(path, target, project_name):
    tmp = path.parent / 'tmp'
    os.makedirs(tmp, exist_ok=True)

    with ZipFile(path) as archive:
        archive.extractall(tmp)

    handle_tree(tmp, target, project_name)
    shutil.rmtree(tmp)
