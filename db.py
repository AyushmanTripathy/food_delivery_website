from sqlite3 import connect

DB_NAME = "database.db"
def execute_query(query, many):
    print("query: ", query)
    conn = connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.execute(query)
    res = cur.fetchall() if many else cur.fetchone()
    conn.commit()
    conn.close()
    print("res: ", res)
    return res

def encode_val(val):
    if type(val) == str:
        return f"'{val}'"
    return str(val)

def encode_list(l):
    return ",".join(map(encode_val, l))

def insert_into(table, columns, values, many = False):
    query = f"insert into {table} ({','.join(columns)}) values ({ encode_list(values) })"
    return execute_query(query, many)

def select_where(table, column, val, many = False):
    query = f"select * from {table} where {column} = { encode_val(val) };"
    return execute_query(query, many)

def select_all(table):
    return execute_query(f"select * from {table};", True)

def select_user_orders(userid):
    query = f"SELECT orders.id, name, price, category from orders join items where user_id = {userid} and orders.item_id = items.id;"
    output, orders = {}, execute_query(query, True)
    for order in orders:
        if order[1] in output:
            output[order[1]][-1] += 1
        else:
            l = list(order)
            l.append(1)
            output[l[1]] = l
    return list(output.values()) 

def delete_row(table, column, val):
    query = f"delete from {table} where {column} = {val};"
    return execute_query(query, False)
