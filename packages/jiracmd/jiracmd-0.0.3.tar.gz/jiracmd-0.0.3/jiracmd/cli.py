import os
import click
from jira import JIRA
from jiracmd import worklog

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    USERNAME = os.getenv('JIRA_USERNAME')
    API_TOKEN = os.getenv('JIRA_API_TOKEN')
    SERVER = os.getenv('JIRA_SERVER')
    ctx.obj = JIRA(server=SERVER, basic_auth=(USERNAME, API_TOKEN))

@click.group(name="worklog")
def cli_worklog():
    pass

@click.group(name="issue")
def cli_issue():
    pass 

@click.command(name="add")
@click.option('-i', '--issue')
@click.option('-s', '--start')
@click.option('-e', '--end')
@click.option('-d', '--date')
@click.option('-t', '--time-spent')
@click.pass_obj
def worklog_add(jira, issue, start, end, date, time_spent):
    click.echo(f'== Worklog: add {issue} on {date} {start}')
    worklog.add()

@click.command(name="list")
@click.pass_obj
@click.option('-i', '--issue')
def worklog_list(jira, issue):
    click.echo(':: Worklog List')
    click.echo(jira)
    worklog.list()


cli.add_command(cli_worklog)
cli.add_command(cli_issue)
cli_worklog.add_command(worklog_list)
cli_worklog.add_command(worklog_add)





if __name__ == "__main__":
    cli()
