# Example script showing different types of interactions with
# objects in CrateDB. This has no hardware dependencies so should 
# run in any MicroPython environment. You will need to edit the
# code below to use your CrateDB credentials.

import microcrate

# CrateDB Docker / local network, no SSL.
# crate = microcrate.CrateDB(host="hostname", use_ssl=False)

# CrateDB Cloud.
# crate = microcrate.CrateDB(
#     host="host", 
#     user="user", 
#     password="password"
# )

crate = microcrate.CrateDB(host="localhost", use_ssl=False)

try:
    # Create a table, using a dynamic object column.
    print("Create table.")
    response = crate.execute("create table driver_object_test (id TEXT, data OBJECT(DYNAMIC))")
    # response:
    # TODO
    print(response)


    # Drop the table.
    print("Drop table...")
    response = crate.execute("drop table driver_test")
    # response:
    # TODO
    print(response)

except microcrate.NetworkError as e:
    print("Caught NetworkError:")
    print(e)
except microcrate.CrateDBError as c:
    print("Caught CrateDBError:")
    print(c)