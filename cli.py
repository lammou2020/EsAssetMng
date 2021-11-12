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
    con = sqlite3.connect('c:/code/ppym.sqlite')
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

@click.command()
def itemlist():
    import sqlite3
    con = sqlite3.connect('c:/code/ppym.sqlite')
    cur = con.cursor()
    cnt=0
    for row in cur.execute(f"SELECT PK,SK,itemtype FROM itemtype where pk like '4271%' order by PK;"):
        #print(row)
        cnt=cnt+1
        if str(row[1])=="4271":
            if cnt>1 :print("</div>")
            print(f'<h3><a href=#>{row[1]} {row[2]}</a></h3>')
            print(f'<div style="margin:0;padding:0;">')
        else:
            print(f'<h4><a href=# onclick="GetNewItemNo({row[0]},this);">{row[0]} {row[2]}</a></h4>')
    if cnt>1 :print("</div>")
        
    pass

cli.add_command(itemlist)
cli.add_command(itRows)
cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()