from invoke import task

@task
def start(ctx):
    ctx.run("gunicorn --config gunicorn_config.py 'app:create_app()'", pty=True)

@task
def lint(ctx):
    print("Linting")
    ctx.run("pylint app", pty=True)

@task
def format(ctx):
    print("Formatting code")
    ctx.run("autopep8 -v --in-place --recursive app", pty=True)

@task
def clean(ctx):
    print("Cleaning")
    ctx.run("pyclean --verbose .", pty=True)

@task
def initdb(ctx):
    print("Initializing database")
    ctx.run("flask --app app init-db", pty=True)

@task
def populatedb(ctx):
    print("Populating database")
    ctx.run("flask --app app populate-db", pty=True)
