from .db_connection import conn

async def db_get_connections():
    async with conn.cursor() as cursor:
        q = """
        SELECT * FROM connections
        ORDER BY id
        """

        await cursor.execute(q)
        results = await cursor.fetchall()
        return [dict(item) for item in results]
    
async def db_create_connection(connection):
    async with conn.cursor() as cursor:
        q = f"""
            INSERT INTO connections(university_identification_number,name)
            VALUES (%s, %s)
            RETURNING *
        """

        await cursor.execute(q, (connection["university_identification_number"], connection["name"]))
        return await cursor.fetchone()

async def remove_record(record_id):
    async with conn.cursor() as cursor:
        q = f"""DELETE FROM connections WHERE id=%s"""
        await cursor.execute(q, (record_id,))
