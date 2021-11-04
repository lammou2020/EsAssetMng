import click

@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Droped the database')

#  @click.option('--tablename', prompt='table name', help='number of rows')

@click.command()
@click.option('--limit', default=1, help='number of rows')
@click.option('--tablename', prompt='table name', help='number of rows')
def itRows(limit,tablename):

    import sqlite3
    con = sqlite3.connect('ppym.sqlite')
    cur = con.cursor()
    if tablename==".tables" :
        for row in cur.execute(f"select name  from sqlite_master where type = 'table'"):#name, sql
            print(row)
    else:
        rows= cur.execute(f"select name  from sqlite_master where type = 'table' and name='{tablename}'") #name, sql
        if len(list(rows))>0 :
            for row in cur.execute(f'SELECT * FROM {tablename}'):
                print(row)
    pass


cli.add_command(itRows)
cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()