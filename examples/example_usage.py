# Example script showing different types of interactions with
# CrateDB. This has no hardware dependencies so should run 
# in any MicroPython environment. You will need to edit the
# code below to use your CrateDB credentials.

import cratedb

# CrateDB Docker / local network, no SSL.
crate = cratedb.CrateDB(host="localhost", use_ssl=False)

# CrateDB Cloud, using SSL.
"""
crate = cratedb.CrateDB(
    host="testdrive.cratedb.net",
    user="username",
    password="password"
)
"""

try:
    # Create a table.
    print("Create table.")
    response = crate.execute("create table driver_test(id TEXT, val1 bigint, val2 bigint, val3 boolean)")
    # response:
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 119.652275}
    print(response)

    # Bulk INSERT.
    print("Bulk insert.")
    response = crate.execute(
        "insert into driver_test (id, val1, val2, val3) values (?, ?, ?, ?)",
        [
            [ "a", 2, 3, True ],
            [ "b", 3, 4, False ]
        ]
    )
    # response:
    # {'results': [{'rowcount': 1}, {'rowcount': 1}], 'cols': [], 'duration': 6.265751}
    print(response)

    # Basic SELECT, also returning column data types.
    print("Select with column data types.")
    response = crate.execute("select * from driver_test", with_types=True)
    # response:
    # {'col_types': [4, 10, 10, 3], 'cols': ['id', 'val1', 'val2', 'val3'], 'rowcount': 2, 'rows': [['b', 3, 4, False], ['a', 2, 3, True]], 'duration': 4.378391}
    print(response)

    # SELECT with parameter substitution.
    print("Select with parameter substitution.")
    response = crate.execute(
        "select val1, val2 from driver_test where val1 > ? and val2 < ?",
        [ 1, 4 ]
    )
    # response:
    # {'rows': [[2, 3]], 'rowcount': 1, 'cols': ['val1', 'val2'], 'duration': 3.266117}
    print(response)

    # INSERT with parameter substitution.
    print("Insert with parameter substitution.")
    response = crate.execute(
        "insert into driver_test (id, val1, val2, val3) values (?, ?, ?, ?)",
        [ "d", 1, 9, False ]
    )
    # response:
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 5.195949}
    print(response)

    # INSERT with parameter substitution, no parsing or return of response document.
    print("Insert with parameter substitution and no response processing.")
    response = crate.execute(
        "insert into driver_test (id, val1, val2, val3) values (?, ?, ?, ?)",
        [ "e", 4, 12, True ],
        return_response=False
    )
    # response:
    # None
    print(response)

    # Drop the table.
    print("Drop table...")
    response = crate.execute("drop table driver_test")
    # response:
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 32.84445}
    print(response)

    # This will throw a CrateDBError as we dropped the table.
    response = crate.execute("select * from driver_test")

except cratedb.NetworkError as e:
    print("Caught NetworkError:")
    print(e)
except cratedb.CrateDBError as c:
    print("Caught CrateDBError:")
    print(c)
