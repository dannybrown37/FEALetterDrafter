from functions.validate import menu_choice


def query_entire_table(dbm):
    sql = """ SELECT name FROM sqlite_master WHERE type = 'table' """
    results = dbm.query(sql)
    tables = [name[0] for name in results]
    prompt = "From which table would you like to select?"
    print
    for x in range(1, len(tables)+1):
        print str(x) + ". " + tables[x-1]
    table = menu_choice(prompt, str(range(len(tables)+1)))

    sql = """ SELECT * FROM %s """ % tables[table-1]
    results = dbm.query(sql)
    for line in results:
        print line
