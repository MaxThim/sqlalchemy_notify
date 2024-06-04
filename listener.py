import psycopg
import asyncio
import sys


DATABASE_URL = "postgresql://postgres:1234@localhost/todo_db"

async def listen_notifications():
    connection = await psycopg.AsyncConnection.connect(DATABASE_URL, autocommit=True)
    cursor = connection.cursor()
    await cursor.execute("LISTEN object_changes;")
    print("Waiting for notifications on channel 'object_changes'...")
    while True:
        async for notification in connection.notifies():
            action, object_id = notification.payload.split()
            print(f"Received notification: {notification.payload}")
            await cursor.execute(f"SELECT name FROM simple_object WHERE id = {object_id};")
            result = await cursor.fetchone()
            if result:
                name = result[0]
                if action == "CREATE":
                    print(f"Created {name}")
                elif action == "UPDATE":
                    print(f"Updated {name}")
            else:
                print(f"No object found with id {object_id}") 


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(listen_notifications())  # Use asyncio.run() to run the async function
