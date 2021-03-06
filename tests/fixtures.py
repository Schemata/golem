import os
import shutil
import random
import string
from subprocess import call

import pytest



# this is deprecated, sould be @pytest.fixture
# but travis uses an old version of pytest for python 3.4
@pytest.yield_fixture(scope="session")
def testdir_fixture():    
    base_dir = os.getcwd()
    test_dir_name = 'temp_directory1'
    full_path = os.path.join(base_dir, test_dir_name)
    if os.path.exists(full_path):
        shutil.rmtree(test_dir_name)
    call(['golem-admin', 'createdirectory', test_dir_name])
    yield {
            'path': full_path,
            'base_path': base_dir,
            'name': test_dir_name}
    os.chdir(base_dir)
    shutil.rmtree(test_dir_name, ignore_errors=True)


@pytest.mark.usefixtures("testdir_fixture")
@pytest.yield_fixture(scope="session")
def project_fixture(testdir_fixture):
    project_name = 'temp_project1'
    os.chdir(testdir_fixture['name'])
    call(['python', 'golem.py', 'createproject', project_name])
    yield {
            'testdir_fixture': testdir_fixture,
            'name': project_name}
    os.chdir(os.path.join(testdir_fixture['path'], 'projects'))
    shutil.rmtree(project_name)


@pytest.mark.usefixtures("testdir_fixture")
@pytest.yield_fixture(scope="class")
def random_project_fixture(testdir_fixture):
    random_value = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    random_name = 'project_' + random_value
    os.chdir(testdir_fixture['name'])
    call(['python', 'golem.py', 'createproject', random_name])
    yield {
            'testdir_fixture': testdir_fixture,
            'name': random_name}
    os.chdir(os.path.join(testdir_fixture['path'], 'projects'))
    shutil.rmtree(random_name)
