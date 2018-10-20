CREATE_TASK = """
    INSERT INTO TASKS(CREATE_TIME)
    VALUES(NOW())
    RETURNING ID;
"""

INSPECT_TASK = """
    SELECT *
    FROM TASKS
    WHERE ID = %s
"""

# preventing race conditions via "SKIP LOCKED"
# fair task execution order is provided via "ORDER BY ID"
TAKE_TASK = """
    SELECT ID
    FROM TASKS
    WHERE START_TIME IS NULL
    ORDER BY ID
    FOR UPDATE SKIP LOCKED
    LIMIT 1;
"""

RUN_TASK = """
    UPDATE TASKS
    SET START_TIME = NOW()
    WHERE ID = %s;
"""

FINISH_TASK = """
    UPDATE TASKS
    SET EXEC_TIME = NOW()
    WHERE ID = %s;
"""
