#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
sqlite 常用方法
'''


def check_table_exist(conn, table):
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM sqlite_master WHERE type={0} AND name={1}'.format("'table'", "'%s'"%table))
    dataset = cursor.fetchall()
    cursor.close()
    if dataset and dataset[0] and dataset[0][0]:
        return True
    else:
        return False

def create_table(conn, table, fields, int_primary_field=None):
    if int_primary_field:
        fields = [x for x in fields if not x == int_primary_field]
        sql_create = 'create table {0} ({1} integer primary key, {2})'.format(table, int_primary_field, ', '.join(fields))
    else:
        sql_create = 'create table {0} ({1})'.format(table, ', '.join(fields))
    cursor = conn.cursor()
    cursor.execute(sql_create)
    conn.commit()
    cursor.close()
