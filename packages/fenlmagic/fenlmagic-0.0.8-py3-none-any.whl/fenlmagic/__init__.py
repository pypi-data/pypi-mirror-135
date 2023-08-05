#!/bin/python

"""
Copyright (C) 2021 Kaskada Inc. All rights reserved.

This package cannot be used, copied or distributed without the express
written permission of Kaskada Inc.

For licensing inquiries, please contact us at info@kaskada.com.
"""

from __future__ import print_function
import IPython
from IPython.core.error import UsageError
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)

import os
import pandas
import argparse

import kaskada as kda
from kaskada import compute
import kaskada.api.v1alpha.compute_pb2 as pb

from google.protobuf.json_format import MessageToJson

class QueryResult(object):
    dataframe: pandas.DataFrame = None

    def __init__(self, query: str, result_url: str):
        self.query = query
        self.result_url = result_url

    def set_dataframe(self, dataframe: pandas.DataFrame):
        self.dataframe = dataframe

@magics_class
class FenlMagics(Magics):

    client = None
    tables = {}
    views = {}

    def __init__(self, shell, client):
        super(FenlMagics, self).__init__(shell)
        self.client = client

    @line_magic
    @magic_arguments()
    @argument('--plaintext', default=False, action='store_true', help='Connects to the given endpoint without TLS encryption')
    @argument('--legacy', default=False, action='store_true', help='Uses the legacy compute engine')
    @argument('--endpoint', default="api.kaskada.com:50051", type=str, help='The Kaskada endpoint and port.')
    @argument('--exchange-endpoint', default="prod-kaskada.us.auth0.com", type=str, help='The Auth endpoint to use when obtaining a JWT.')
    @argument('--audience', default="https://api.prod.kaskada.com", type=str, help='The Auth audience to use when obtaining a JWT.')
    @argument('client_id', metavar='client-id', type=str, help='The Kaskada credential Client-ID.')
    @argument('client_secret', metavar='client-secret', type=str, help='The Kaskada credential Client-Secret.')
    def fenl_auth(self, arg):
        "fenl API client id"

        args = parse_argstring(self.fenl_auth, arg)

        self.client = kda.client(
            client_id = args.client_id,
            client_secret = args.client_secret,
            endpoint = args.endpoint,
            exchange_endpoint = args.exchange_endpoint,
            audience = args.audience,
            is_secure = not args.plaintext,
            engine = "LEGACY" if args.legacy else None
        )

    @cell_magic
    @magic_arguments()
    @argument('name', type=str, help='The table name.')
    @argument('schema', type=str, help='The table schema.')
    @argument('entity', type=str, help='The table entity expression.')
    @argument('time', type=str, help='The table time expression.')
    def fenl_table(self, arg, cell):
        "adds a named table to all subsequent fenl queries"

        args = parse_argstring(self.fenl_table, arg)
        name = args.name.strip('"').strip("'")
        entity = args.entity.strip('"').strip("'")
        time = args.time.strip('"').strip("'")
        schema = args.schema.strip('"').strip("'")

        t = pb.WithTable(
            name = name,
            entity = entity,
            time = time,
        )
        t.json_values.schema = schema.strip('"').strip("'")
        t.json_values.values.extend(cell.splitlines())

        self.tables[args.name] = t

    @magic_arguments()
    @argument('--as-view', help='adds the body as a view with the given name to all subsequent fenl queries.')
    @argument('--data-token', help='A data token to run queries against. Enables repeatable queries.')
    @argument('--debug', default=False, help='Shows debugging information')
    @argument('--output', help='Output format for the query results. One of "df" (default), "json", "parquet" or "redis-bulk".  "redis-bulk" implies --result-behavior "final-results"')
    @argument('--preview-rows', help='Produces a preview of the data with at least this many rows.')
    @argument('--result-behavior', help='Determines which results are returned. Either "all-results" (default), or "final-results" which returns only the final values for each entity.')
    @argument('--var', help='Assigns the body to a local variable with the given name')
    @argument('--resume-token', help='A resume token to run queries against. Used with the --data-token to enable resumeable queries.')
    @cell_magic
    @line_cell_magic
    def fenl(self, arg, cell = None):
        "fenl query magic"

        args = parse_argstring(self.fenl, arg)
        output = clean_arg(args.output)
        result_behavior = clean_arg(args.result_behavior)
        preview_rows = clean_arg(args.preview_rows)
        var = clean_arg(args.var)
        view = clean_arg(args.as_view)

        with_tables = []
        with_views = []

        if cell == None:
            with_views.extend(self.views.values())
            query = arg

        else:
            if view is not None:
                v = pb.WithView(
                    name = view,
                    expression = cell,
                )
                self.views[view] = v
                query = view

            else:
                query = cell.strip()

        with_tables.extend(self.tables.values())
        with_views.extend(self.views.values())

        limits = {}
        if preview_rows:
            limits['preview_rows'] = int(preview_rows)

        try:
            resp = compute.query(
                query=query,
                with_tables=with_tables,
                with_views=with_views,
                result_behavior= 'final-results' if test_arg(result_behavior, 'final-results') else 'all-results',
                data_token_id=clean_arg(args.data_token),
                resume_token=clean_arg(args.resume_token),
                response_as= 'redis-bulk' if test_arg(output, 'redis-bulk') else 'parquet',
                limits=pb.QueryRequest.Limits(**limits),
                client=self.client
            )

            if resp.data_token_id:
                print(f'data_token_id: "{resp.data_token_id}"')

            if resp.next_resume_token:
                print(f'next_resume_token: "{resp.next_resume_token}"')

            if resp.request_details and resp.request_details.request_id:
                print(f'request_details {{\n  request_id: "{resp.request_details.request_id}"\n}}')

            result = None
            if test_arg(output, 'redis-bulk'):
                query_result = QueryResult(query, resp.redis_bulk.path)
                result = query_result.result_url
            elif test_arg(output, 'parquet'):
                query_result = QueryResult(query, resp.parquet.path)
                result = query_result.result_url
            else:
                query_result = QueryResult(query, resp.parquet.path)
                df = pandas.read_parquet(query_result.result_url, engine='pyarrow')
                if args.debug:
                    query_result.set_dataframe(df)
                    return df

                query_result.set_dataframe(df.drop(['_time', '_subsort', '_key_hash'], axis=1))
                result = query_result.dataframe

            if var is not None:
                IPython.get_ipython().push({var : query_result})

            return result
        except Exception as e:
            raise UsageError(e)

def load_ipython_extension(ipython):
    if kda.KASKADA_DEFAULT_CLIENT is None:
        if os.getenv('KASKADA_CLIENT_ID') and os.getenv('KASKADA_CLIENT_SECRET'):
            kda.init()

    magics = FenlMagics(ipython, kda.KASKADA_DEFAULT_CLIENT)
    ipython.register_magics(magics)

def clean_arg(arg : str) -> str:
    """
    Strips quotes and double-quotes from passed arguments

    Args:
        arg (str): input argument

    Returns:
        str: cleaned output
    """
    if arg is not None:
        return arg.strip('"').strip("'")
    else:
        return None

def test_arg(arg: str, val: str) -> bool:
    """Compares an argument against a test value.  Returns true when the two strings are equal in a case-insenstive and dash/underscore-insensitive manner.

    Args:
        arg (str): the argument to test
        val (str): the comparison value

    Returns:
        bool: The comparision result.
    """
    if arg is not None and val is not None:
        return arg.replace('_','-').lower() == val.replace('_','-').lower()

# def unload_ipython_extension(ipython):
