# Example script showing different types of interactions with
# objects in CrateDB. This has no hardware dependencies so should 
# run in any MicroPython environment. You will need to edit the
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
    print("Drop any previous table.")
    crate.execute("DROP TABLE IF EXISTS driver_object_test", return_response=False)

    # Create a table, using a dynamic object column.
    print("Create table.")
    response = crate.execute("CREATE TABLE driver_object_test (id TEXT PRIMARY KEY, data OBJECT(DYNAMIC))")

    # response:
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 270.4579}
    print(response)

    # Insert an object with arbitrary complexity.
    print("INSERT a row containing an object.")
    example_obj = {
        "sensor_readings": {
            "temp": 23.3,
            "humidity": 61.2
        },
        "metadata": {
            "software_version": "1.19",
            "battery_percentage": 57,
            "uptime": 2851200
        }
    }

    response = crate.execute(
        "INSERT INTO driver_object_test (id, data) VALUES (?, ?)",
        [
            "2cae54",
            example_obj
        ]
    )

    # response: 
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 334.37607}
    print(response)

    # Select query returning the entire object.
    print("SELECT the whole object.")
    response = crate.execute(
        "SELECT data FROM driver_object_test WHERE id = ?",
        [
            "2cae54"
        ]
    )

    # response:
    # {'rows': [
    #     [{
    #         'metadata': {'software_version': '1.19', 'uptime': 2851200, 'battery_percentage': 57}, 
    #         'sensor_readings': {'humidity': 61.2, 'temp': 23.3}}
    #     ]
    #  ], 'rowcount': 1, 'cols': ['data'], 'duration': 21.946375
    # }
    print(response)

    # Select query returning some fields from the object.
    print("SELECT some parts of the object but not all.")
    response = crate.execute(
        """SELECT 
                id,
                data['metadata']['uptime'] AS uptime, 
                data['sensor_readings'] AS sensor_readings 
           FROM driver_object_test 
           WHERE id = ?""",
        [
            "2cae54"
        ]
    )

    # response:
    # {'rows': [
    #     [2851200, {'humidity': 61.2, 'temp': 23.3}]
    #  ], 
    #  'rowcount': 1, 'cols': ['uptime', 'sensor_readings'], 'duration': 4.047666
    # }
    print(response)

    # Bulk insert additional objects.
    response = crate.execute(
        "INSERT INTO driver_object_test (id, data) VALUES (?, ?)",
        [
            [ 
                "2cae56", 
                {
                    "sensor_readings": {
                    "temp": 21.8,
                    "humidity": 57.9
                    },
                    "metadata": {
                        "software_version": "1.19",
                        "battery_percentage": 43,
                        "uptime": 2851643
                    }
                } 
            ],
            [
                "1d452b", 
                {
                    "sensor_readings": {
                        "temp": 11.4,
                        "humidity": 43.9
                    },
                    "metadata": {
                        "software_version": "1.20",
                        "battery_percentage": 17,
                        "uptime": 853436
                    }
                } 
            ],
            [ 
                "4e000f", 
                {
                    "sensor_readings": {
                        "temp": 26.8,
                        "humidity": 78.9
                    },
                    "metadata": {
                        "software_version": "1.19",
                        "battery_percentage": 84,
                        "uptime": 1468356
                    },
                } 
            ]
        ]
    )

    # response:
    # {'results': [
    #     {'rowcount': 1}, 
    #     {'rowcount': 1}, 
    #     {'rowcount': 1}
    #  ], 'cols': [], 'duration': 4.426417
    # }
    print(response)

    # Tells the database to refresh the table.  This is here to make sure that the
    # subsequent SELECT has the data from the INSERT above.  This is not needed in
    # real application code.  
    # See https://cratedb.com/docs/crate/reference/en/latest/sql/statements/refresh.html
    # for details.
    crate.execute("REFRESH TABLE driver_object_test", return_response=False)


    # SELECT example that filters by an object property in the WHERE clause.
    print("SELECT and filter by an object property in the WHERE clause.")
    response = crate.execute(
        """
            SELECT id, data['sensor_readings'] AS sensor_readings FROM driver_object_test 
            WHERE data['metadata']['software_version'] = '1.19'
        """
    )

    # response:
    # { 'rows': [
    #     ['4e000f', {'humidity': 78.90000000000001, 'temp': 26.8}], 
    #     ['2cae54', {'humidity': 61.2, 'temp': 23.3}], 
    #     ['2cae56', {'humidity': 57.9, 'temp': 21.8}]
    #   ], 'rowcount': 3, 'cols': ['id', 'sensor_readings'], 'duration': 13.790875}
    print(response)

    # Add some sample data about different countries in South America, their
    # borders and currency exchange rates.
    print("Add country data for Colombia and Brazil.")
    response = crate.execute(
        """
            INSERT INTO driver_object_test (id, data) VALUES (?, ?)
        """,
        [
            [
                "co",
                {
                    "name": "Colombia",
                    "borders": [
                        "Brazil", "Peru", "Panama", "Ecuador", "Venezuela"
                    ],
                    "currency": {
                        "code": "COP",
                        "name": "Colobian Peso"
                    },
                    "rates": [
                        {
                            "code": "USD",
                            "rate": "0.000235"
                        },
                        {
                            "code": "EUR",
                            "rate": "0.000216"
                        },
                        {
                            "code": "JPY",
                            "rate": "0.035154"
                        }
                    ]
                }
            ],
            [
                "br",
                {
                    "name": "Brazil",
                    "borders": [
                        "Argentina", "Bolivia", "Colombia", "French Guiana",
                        "Guyana", "Paraguay", "Suriname", "Uruguay", "Venezuela"
                    ],
                    "currency": {
                        "code": "BRL",
                        "name": "Brazilian Real"
                    },
                    "rates": [
                        {
                            "code": "USD",
                            "rate": "0.176620"
                        },
                        {
                            "code": "EUR",
                            "rate": "0.162409"
                        },
                        {
                            "code": "JPY",
                            "rate": "26.432108"
                        }
                    ]
                }
            ]
        ]
    )

    # response:
    # {'results': [{'rowcount': 1}, {'rowcount': 1}], 'cols': [], 'duration': 46.436874}
    print(response)

    # Some examples showing how to access data inside arrays.
    # See also https://cratedb.com/docs/crate/reference/en/latest/general/builtins/scalar-functions.html#array-functions
    
    # Simple array... which countries does Colombia share a border with?
    print("Arrays... countries sharing a border with Colombia.")
    response = crate.execute(
        """
            SELECT data['borders'] as shares_border_with FROM driver_object_test WHERE id = 'co'
        """
    )

    # response:
    # {'rows': [[['Brazil', 'Peru', 'Panama', 'Ecuador', 'Venezuela']]], 'rowcount': 1, 'cols': ['shares_border_with'], 'duration': 50.105873}
    print(response)

    # How many countries does Brazil share a border with?
    print("How many entries are in an array?")
    response = crate.execute(
        # 1 here is the array dimension to get the length of, as arrays can be nested.
        """
            SELECT array_length(data['borders'], 1) as how_many FROM driver_object_test WHERE id = 'br'
        """
    )

    # response:
    # {'rows': [[9]], 'rowcount': 1, 'cols': ['how_many'], 'duration': 1.397291}
    print(response)

    # What are the 2nd, 3rd and 4th countries in Brazil's borders array? (Arrays are 1 indexed).
    print("Array slicing.")
    response = crate.execute(
        """
            SELECT array_slice(data['borders'], 2, 4) AS slice FROM driver_object_test WHERE id = 'br'
        """
    )

    # response:
    # {'rows': [[['Bolivia', 'Colombia', 'French Guiana']]], 'rowcount': 1, 'cols': ['slice'], 'duration': 1.517417}
    print(response)

    # Example queries for arrays containing objects.
    # Retrieve the currency code for the 2nd currency rate object in the rates array.
    # Remember, arrays are 1 indexed.

    print("Mixing objects and arrays...")
    response = crate.execute(
        """
            SELECT data['rates'][2]['code'] FROM driver_object_test WHERE id='co'
        """
    )

    # response:
    # {'rows': [['EUR']], 'rowcount': 1, 'cols': ["data[2]['rates']['code']"], 'duration': 0.553541}
    print(response)

    # Array comparisons. 
    # https://cratedb.com/docs/crate/reference/en/latest/general/builtins/array-comparisons.html#sql-array-comparisons
    # Which countries share a border with Paraguay?
    print("Element in array: Who shares a border with Paraguay?")

    response = crate.execute(
        """
            SELECT data['name'] AS name, 'Paraguay' IN (data['borders']) AS borders_paraguay 
            FROM driver_object_test WHERE id IN ('br', 'co')
        """
    )

    # response:
    # {'rows': [['Colombia', False], ['Brazil', True]], 'rowcount': 2, 'cols': ['name', 'borders_paraguay'], 'duration': 0.574833}
    print(response)

    # Drop the table.
    print("Drop table...")
    response = crate.execute("DROP TABLE driver_object_test")
    # response:
    # {'rows': [[]], 'rowcount': 1, 'cols': [], 'duration': 67.91708}
    print(response)

except cratedb.NetworkError as e:
    print("Caught NetworkError:")
    print(e)
except cratedb.CrateDBError as c:
    print("Caught CrateDBError:")
    print(c)