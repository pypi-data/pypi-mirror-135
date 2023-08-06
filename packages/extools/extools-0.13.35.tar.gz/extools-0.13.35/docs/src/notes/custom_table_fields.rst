Custom Table Fields Reference
=============================

Custom Tables support a number of different field types.

An example module containing all the types::

    [MODULE]
    id=TEST
    name=Test
    desc=Test
    company=Test

    [TABLE]
    name=TEST.TEST
    desc=Test table to get a handle on field types.
    dbname=TEST

    [FIELD1]
    field=TEXT
    datatype=1
    mask=%-60C
    size=60

    [FIELD2]
    field=DATE
    datatype=3

    [FIELD3]
    field=TIME
    datatype=4

    [FIELD4]
    field=INT16
    datatype=7

    [FIELD5]
    field=INT32
    datatype=8

    [FIELD6]
    field=BOOL
    datatype=9

    [FIELD7]
    field=NUMBER #aka BCD
    datatype=6
    size=10
    decimals=0

    [KEY1]
    KEYNAME=KEY1
    FIELD1=TEXT
    allowdup=0
