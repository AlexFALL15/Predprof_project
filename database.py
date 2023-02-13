import sqlite3

def make_stroke(comp, org, date, file_name):
    con = sqlite3.connect('competitions.db')
    cur = con.cursor
    cur.execute(f"""insert into comps(comp_name, organisator, date, file) values('{comp}', '{org}', '{date}', '{file_name}')""")
    con.close()

def get_file(comp):
    con = sqlite3.connect('competitions.db')
    cur = con.cursor
    result = cur.execute(f"""select from comps file
                         where comp='{comp}'""").fetchall()
    con.close()
    return result[0]