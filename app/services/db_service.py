import main


def get_row(table: str, criteria: dict | None):
    query = f"SELECT * FROM {table} WHERE"

    if criteria != {}:
        criteria_keys = criteria.keys()

        i = 1
        for key in criteria_keys:
            if i > 1:
                query += ","
            query += f" {key} = %s"
            i += 1

    print(query, tuple(criteria.values()))

    main.cursor.execute(query, tuple(criteria.values()))

    return main.cursor.fetchall()


def add_row(table: str, data: dict):
    query = f"INSERT INTO {table} "

    data_keys = data.keys()
    data_values = data.values()

    query += "("
    i = 1
    for key in data_keys:
        if i > 1:
            query += ","
        query += f" {key}"
        i += 1

    query += ") values ("

    j = 1
    for _ in data_values:
        if j > 1:
            query += ","
        query += " %s"
        j += 1

    query += ") RETURNING *"

    main.cursor.execute(query, tuple(data.values()))

    return main.conn.commit()
