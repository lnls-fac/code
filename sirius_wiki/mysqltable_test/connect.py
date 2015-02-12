#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parameter import Parameter
import mysql.connector

sirius_database = {'host':'10.0.21.152', 'user':'prm_editor', 'password':'prm0', 'database':'parameters'}

def parameter_exist(cursor, parameter_name):
    query  = ("SELECT COUNT(1) FROM parameter WHERE name='" + parameter_name + "' LIMIT 1")
    cursor.execute(query)
    result = cursor.fetchone()
    if result[0] == 0:
        return False
    else:
        return True

def insert_parameter(cursor, parameter):
    query  = u'INSERT INTO parameter '
    query += u'(name, team, symbol, value, units, deps, obs) VALUES ('
    query += parameter.name
    query += u',' + parameter.group
    query += u',' + parameter.symbol
    query += u',' + parameter.value
    query += u',' + parameter.units
    query += u',' + parameter.deps
    query += u',' + parameter.obs
    query += ')'
    cursor.execute(query)

 function build_update_query($db_fields)
    {
        $query = "UPDATE parameter SET " .
            "team='" . $db_fields['group'] . "', " .
            "symbol='" . $db_fields['symbol'] . "', " .
            "units='" . $db_fields['units'] . "', " .
            "is_derived='" . $db_fields['is_derived'] . "', " .
            "value='" . $db_fields['value'] . "' " .
            "WHERE name='" . $db_fields['name'] . "';";

        return $query;
    }


def update_parameter(cursos, parameter):
    query  = u'UPDATE parameter SET '
    query += 'team=' + parameter.group
    query += 'team=' + parameter.



cnx = mysql.connector.connect(**sirius_database)
cursor = cnx.cursor()


p = Parameter(name='SI lattice version', group='FAC', value='V04', symbol='', units='', deps=[], obs=[], ),
print(p.__dict__)

flag = parameter_exist(cursor, 'BO random normal 8-pole error tolerance for dipoles')
print(flag)
flag = parameter_exist(cursor, 'BO random normal 8-pole error tolerannce for dipoles')
print(flag)

cursor.close()
cnx.close()

    
