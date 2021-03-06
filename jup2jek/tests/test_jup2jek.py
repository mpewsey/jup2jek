import os
import pytest
from subprocess import check_output
from .. import Jup2Jek, Jup2JekArgParser


def root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def jup2jek_init():
    p = root_dir()
    return Jup2Jek(p)


def jup2jek_init_options():
    p = root_dir()
    return Jup2Jek(p, 'jup2jek.ini')


def test_bad_options_path():
    p = root_dir()
    with pytest.raises(Exception):
        Jup2Jek(p, 'bad_file_name.ini')


def test_write_default_options():
    p = root_dir()
    Jup2Jek.write_default_options(p)
    assert os.path.exists(p) == True


def test_load_options():
    j = jup2jek_init()
    assert j.options == {'posts': '_posts',
                         'assets': 'assets/jupyter'}


def test_notebooks():
    j = jup2jek_init()
    p = root_dir()
    nb = set(os.path.relpath(x, p) for x in j.notebooks())
    assert nb == {'_posts/example1.ipynb',
                  '_posts/example2.ipynb',
                  '_posts/example3.ipynb',
                  '_posts/category1/example4.ipynb'}


def test_create_assets_path():
    j = jup2jek_init()
    j._create_assets_path()
    p = root_dir()
    p = os.path.join(p, 'assets/jupyter')
    assert os.path.exists(p) == True


def test_remove_assets_path():
    j = jup2jek_init()
    j._create_assets_path()
    j._remove_assets_path()
    p = root_dir()
    p = os.path.join(p, 'assets/jupyter')
    assert os.path.exists(p) == False


def test_convert_notebooks():
    j = jup2jek_init()
    j.convert_notebooks()


def test_convert_options():
    j = jup2jek_init_options()
    j.convert_notebooks()


def test_script():
    p = root_dir()
    check_output('jup2jek', cwd=p, shell=True)


def test_script_options():
    p = root_dir()
    options = os.path.join(p, 'jup2jek.ini')
    command = 'jup2jek --options {}'.format(options)
    check_output(command, cwd=p, shell=True)


def test_arg_parser():
    command = ['--options', 'jup2jek.ini']
    p = Jup2JekArgParser()
    a = p.parse_args(command)
    assert a.options == 'jup2jek.ini'
