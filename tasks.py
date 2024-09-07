from invoke import task

@task
def start(ctx):
    ctx.run("gunicorn --config gunicorn_config.py --chdir app app:app", pty=True)
