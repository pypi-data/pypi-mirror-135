from typing import Dict, List
from functools import reduce
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


class DynamoClient:
    def __init__(self, table_name: str, partition_key: str, field_types: Dict, sort_keys: List[str] = None,
                 global_second_indexes: Dict = None):
        self._table_name = table_name
        self._partition_key = partition_key
        self._field_types = field_types
        self._sort_keys = sort_keys
        self._global_second_indexes = global_second_indexes
        self._client = boto3.resource('dynamodb')

    def _get_table(self):
        attribute_definition, key_schema = _compose_creation_parameters(self._field_types,
                                                                        self._partition_key, self._sort_keys,
                                                                        self._global_second_indexes)
        global_second_indexes = _compose_global_second_indexes(self._global_second_indexes)

        try:
            table = self._client.create_table(
                TableName=self._table_name,
                AttributeDefinitions=attribute_definition,
                KeySchema=key_schema,
                BillingMode='PAY_PER_REQUEST',
                GlobalSecondaryIndexes=global_second_indexes,
            )
            table.wait_until_exists()

        except ClientError:
            return self._client.Table(self._table_name)

        return table

    def query_with_index(self, index_name, expr, limit=10):
        table = self._get_table()
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=expr,
            ScanIndexForward=True,
            Limit=limit
        )

        return response.get('Items', [])

    def query_with_key(self, key_expr: Key, limit=10):
        table = self._get_table()
        response = table.query(
            KeyConditionExpression=key_expr,
            ScanIndexForward=True,
            ConsistentRead=True,
            Limit=limit
        )

        return response.get('Items', [])

    def put_item(self, item):
        table = self._get_table()

        # if condition:
        #     condition_expr = reduce((lambda t, s: t & s), [Attr(key).eq(value) for key, value in condition.items()])
        # else:
        #     condition_expr = None
        #
        # if data:
        #     attributes = {key: {'Value': value, 'Action': 'PUT'} for key, value in data.items()}
        # else:
        #     attributes = None

        table.put_item(Item=item)


def _compose_creation_parameters(field_types, partition_key, sort_keys=None, global_second_indexes=None):
    sort_keys = set(sort_keys) if sort_keys else set()
    global_second_index_sets = [set(indexes) for indexes in global_second_indexes.values()]
    global_second_index_names = reduce(_union, global_second_index_sets, set())

    attr_def_names = {partition_key} | sort_keys | global_second_index_names
    attribute_definition = [
        {'AttributeName': key, 'AttributeType': field_types[key]} for key in attr_def_names
    ]

    key_schema = [{'AttributeName': partition_key, 'KeyType': 'HASH'}] + \
                 [{'AttributeName': key, 'KeyType': 'RANGE'} for key in sort_keys]

    return attribute_definition, key_schema


def _compose_global_second_indexes(indexes):
    if not indexes:
        return None

    result = []
    for name, index in indexes.items():
        result.append({
            'IndexName': name,
            'KeySchema': [
                {'AttributeName': index[0], 'KeyType': 'HASH'},
                {'AttributeName': index[1], 'KeyType': 'RANGE'},
            ],
            'Projection': {
                'ProjectionType': 'ALL',
            },
        })
    return result


def _union(t, s):
    return t | s
