from .db_connection import conn

async def db_get_connections():
    async with conn.cursor() as cursor:
        q = """
        SELECT * FROM connections
        ORDER BY connection_time
        """

        await cursor.execute(q)
        results = await cursor.fetchall()
        return [dict(item) for item in results]
    
async def db_create_connection(mac_address, name):
    async with conn.cursor() as cursor:
        q = f"""
            INSERT INTO connections(mac_address,name)
            VALUES (%s, %s)
            RETURNING *
        """

        await cursor.execute(q, (mac_address, name))
        return await cursor.fetchone()
