#!/usr/bn/env python
# -*- coding: utf-8 -*-
# python -m pwiz -H 138.197.210.129 -e mysql -u wikiuser -P password wikidb

from __future__ import print_function
import config

Senators_DB = 'cargo__state_senators'
AssemblyMembers_DB = 'cargo__state_representative'

from peewee import *

database = MySQLDatabase(config.DB_SERVER,
                         **{'host': config.DB_HOST,
                            'password': config.DB_PASSWORD,
                            'user': config.DB_USER})


class BaseModel(Model):
    class Meta:
        database = database


class CargoStateSenator(BaseModel):
    _id = IntegerField(db_column='_ID', unique=True)
    _pageid = IntegerField(db_column='_pageID', index=True)
    _pagename = CharField(db_column='_pageName', index=True)
    _pagenamespace = IntegerField(db_column='_pageNamespace', index=True)
    _pagetitle = CharField(db_column='_pageTitle', index=True)
    active = IntegerField(null=True)
    birth_date = CharField(null=True)
    birth_place = CharField(null=True)
    district = CharField(null=True)
    education = CharField(null=True)
    email = CharField(null=True)
    footnotes = TextField(null=True)
    leg = CharField(db_column='leg_id', null=True)
    name = CharField(null=True)
    occupation = CharField(null=True)
    party = CharField(null=True)
    predecessor = CharField(null=True)
    profession = CharField(null=True)
    residence = CharField(null=True)
    term_end = DateField(null=True)
    term_end__precision = IntegerField(null=True)
    term_start = DateField(null=True)
    term_start__precision = IntegerField(null=True)
    website = CharField(null=True)

    class Meta:
        db_table = 'cargo__state_senators'
        primary_key = False


class CargoPages(BaseModel):
    page = IntegerField(db_column='page_id', index=True)
    table_name = CharField()

    class Meta:
        db_table = 'cargo_pages'
        primary_key = False


class CargoTables(BaseModel):
    field_helper_tables = TextField()
    field_tables = TextField()
    main_table = CharField(unique=True)
    table_schema = TextField()
    template = IntegerField(db_column='template_id', unique=True)

    class Meta:
        db_table = 'cargo_tables'
        primary_key = False


class User(BaseModel):
    user_editcount = IntegerField(null=True)
    user_email = TextField(index=True)
    user_email_authenticated = CharField(null=True)
    user_email_token = CharField(index=True, null=True)
    user_email_token_expires = CharField(null=True)
    user = PrimaryKeyField(db_column='user_id')
    user_name = CharField(unique=True)
    user_newpass_time = CharField(null=True)
    user_newpassword = TextField()
    user_password = TextField()
    user_password_expires = CharField(null=True)
    user_real_name = CharField()
    user_registration = CharField(null=True)
    user_token = CharField()
    user_touched = CharField()

    class Meta:
        db_table = 'user'
