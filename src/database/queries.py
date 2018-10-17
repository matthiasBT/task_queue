CREATE_TASK = """
    INSERT INTO TASKS(CREATE_TIME)
    VALUES(NOW())
    RETURNING ID;
"""

RETRIEVE_TASK = """
    SELECT *
    FROM TASKS
    WHERE ID = %s
"""

TAKE_TASK = """
    SELECT ID
    FROM TASKS
    WHERE START_TIME IS NULL
    FOR UPDATE SKIP LOCKED;  -- preventing race conditions
"""

# now() or null
RUN_TASK_OR_GIVE_AWAY = """
    UPDATE TASKS
    SET START_TIME = %s
    WHERE ID = %s;
"""

FINISH_TASK = """
    UPDATE TASKS
    SET EXEC_TIME = NOW()
    WHERE ID = %s;
"""
