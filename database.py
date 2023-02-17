import sqlite3

def make_stroke(comp, org, date, file_name):
    con = sqlite3.connect('competitions.db')
    cur = con.cursor()
    cur.execute('INSERT INTO comps(comp_name, organisator, date, file) VALUES (?, ?, ?, ?)', [comp, org, date, file_name])
    con.close()

def check_in(comp, org, date, file_name):
    con = sqlite3.connect('competitions.db')
    cur = con.cursor()
    result = cur.execute(f"""select id from comps
                             where comp_name='{comp}' and organisator='{org}' and date={date} and file='{file_name};'""").fetchall()
    con.close()
    return result


if __name__ == "__main__":
    print(check_in('firstcomp', 'Alex', '2023-02-17', 'firstcomp.json'))