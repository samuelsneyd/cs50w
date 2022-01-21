# SQL

### SQLite data types
    TEXT
    NUMERIC
    INTEGER
    REAL
    BLOB (binary)

### MySQL data types
    CHAR(size) (exact size characters)
    VARCHAR(size) (variable size characters up to size)
    SMALLINT
    BIGINT
    FLOAT
    DOUBLE

### CREATE
    CREATE TABLE flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        duration INTEGER NOT NULL
    );

### Constraints
    CHECK (check data obeys a certian condition)
    DEFAULT
    NOT NULL
    PRIMARY KEY
    UNIQUE

### INSERT
    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("New York", "London", 415);

    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("Shanghai", "Paris", 760);

    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("Istanbul", "Tokyo", 700);

    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("New York", "Paris", 435);

    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("Moscow", "Paris", 245);

    INSERT INTO flights
        (origin, destination, duration)
        VALUES ("Lima", "New York", 455);

### SELECT
    SELECT * FROM flights;
    SELECT origin, destination FROM flights;
    SELECT * FROM flights WHERE id = 3;
    SELECT * FROM flights WHERE origin = "New York";

### UPDATE
    UPDATE FLIGHTS
        SET duration = 430
        WHERE origin = "New York"
        AND destination = "London";

### DELETE
    DELETE FROM flights
        WHERE destination = "Tokyo";

### Other clauses
    LIMIT
    ORDER BY
    GROUP BY
    HAVING

### JOIN
    SELECT first, origin, destination
        FROM flights JOIN passengers
        ON passengers.flight_id = flights.id;

### CREATE INDEX
    CREATE INDEX name_index ON passengers (last);

### SQL Injection
    SELECT * FROM users
        WHERE username = "harry"
        AND password = "12345"; (bad)

    SELECT * FROM users
        WHERE username = "hacker"--"
        AND password = ""; (SQL injection using "--)
    
    SELECT * FROM users
        WHERE username = ?
        AND password = ?
        ("harry", "12345");

### RACE CONDITION
    When two or more threads try to 
    edit the same data simultaneously.

