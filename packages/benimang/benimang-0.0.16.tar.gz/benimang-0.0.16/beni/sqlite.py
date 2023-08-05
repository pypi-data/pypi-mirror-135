from typing import Any

from aiosqlite import Connection


async def db_insert(db: Connection, table: str, data: dict[str, Any]):
    keylist = sorted(data.keys())
    fieldname_list = ','.join([f'`{x}`' for x in keylist])
    placement_list = ','.join(['?' for _ in range(len(keylist))])
    fieldvalue_list = [data[x] for x in keylist]
    async with db.execute(f'INSERT INTO `{table}` ({fieldname_list}) VALUES ({placement_list});', fieldvalue_list) as cursor:
        return cursor.lastrowid


async def db_insert_many(db: Connection, table: str, data_list: list[dict[str, Any]]):
    keylist = sorted(data_list[0].keys())
    fieldname_list = ','.join([f'`{x}`' for x in keylist])
    placement_list = ','.join(['?' for _ in range(len(keylist))])
    fieldvalue_list = [[data[x] for x in keylist] for data in data_list]
    await db.executemany(f'INSERT INTO `{table}` ({fieldname_list}) VALUES ({placement_list});', fieldvalue_list)
