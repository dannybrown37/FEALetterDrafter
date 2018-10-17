from .validate import menu_choice, get_case_number

def query_case(dbm):
    sql = """ SELECT name FROM sqlite_master WHERE type = 'table' """
    results = dbm.query(sql)
    tables = []
    for name in results:
        tables.append(name[0])
    prompt = "Which table would you like to select from?"
    print
    for x in range(1, len(tables)+1):
        print str(x) + ". " + tables[x-1]
    table = menu_choice(prompt, str(range(len(tables)+1)))
    case_number = get_case_number()
    sql = "SELECT * FROM %s WHERE CaseNumber = %s " % (
        tables[table-1],
        case_number
    )
    results = dbm.query(sql)
    types = dbm.get_column_names()
    for tuple in results:
        for type, item in zip(types, tuple):
            print "%s: %s" % (type, item)
