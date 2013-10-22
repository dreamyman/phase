from fabric.api import run, env, local, cd, prefix, sudo

# Create an ssh config in ~/.ssh/config
# Host phase
#     HostName phase.testing.com
#     User username
#
# Also add this line in /etc/sudoers on the server:
# talengi ALL = NOPASSWD: /etc/init.d/apache2

USERNAME = 'talengi'
VENV_HOME = '/home/%s/.virtualenvs/' % USERNAME
env.use_ssh_config = True
env.hosts = ['phase']
env.activate = 'workon phase'
env.directory = '/home/%s/phase' % USERNAME
env.sudo_prefix = 'sudo '


def runserver():
    """Runs the local Django server."""
    runserver = 'python src/manage.py runserver'
    with_local_settings = ' --settings=core.settings.local'
    local(runserver + with_local_settings)


def test(module=""):
    """Launches tests for the whole project."""
    runtests = 'coverage run src/manage.py test {module}'.format(
        module=module
    )
    with_test_settings = ' --settings=core.settings.test'
    local(runtests + with_test_settings)


def docs():
    """Generates sphinx documentation for the project."""
    local('cd docs && make clean && make html')
    local('xdg-open docs/_build/html/index.html')


def check():
    """Checks that everything is fine, useful before deploying."""
    test()
    docs()
    runserver()


def restart_webserver():
    sudo('/etc/init.d/apache2 restart', shell=False)


def deploy(with_data=True):
    """Deploys the project against staging."""
    with cd(env.directory):
        run('git pull')
        with prefix(env.activate):
            collectstatic = 'python src/manage.py collectstatic --noinput'
            syncdb = 'python src/manage.py syncdb --noinput'
            with_production_settings = ' --settings=core.settings.production'
            run('pip install -r requirements/production.txt')
            run(collectstatic + with_production_settings)
            if with_data:
                run('rm phase.db')
                run('rm private/* -Rf')
                run(syncdb + with_production_settings)
    restart_webserver()


def log(filename="admin/log/access.log", backlog='F'):
    """Displays access.log file from staging."""
    run("tail -%s '%s'" % (backlog, filename))


def errors(backlog=200):
    """Displays error.log file from staging."""
    return log("admin/log/error.log", backlog)
