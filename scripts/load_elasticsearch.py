import elasticsearch
import json
import click

from csv import DictReader
from toolz import dissoc
from itertools import count
from elasticsearch.helpers import bulk

nadp_index_name = 'nadp'
nadp_report_type_name = 'nadp_report'

nadp_index_body = {
    "mappings": {
        nadp_report_type_name: {
            "properties": {
                "state": {
                    "type": "keyword"
                },
                "state_abbrev": {
                    "type": "keyword"
                },
                "location_description": {
                    "type": "text"
                },
                "location": {
                    "type": "geo_point"
                },
                "date": {
                    "type": "date",
                    "ignore_malformed": True
                },
                "longitude": {
                    "type": "float"
                },
                "latitude": {
                    "type": "float"
                },
                "description": {
                    "type": "text"
                }
            }
        }
    }
}


def nadp_bulk_action(doc, doc_id):
    return {
        "_op_type": "index",
        "_index": nadp_index_name,
        "_type": nadp_report_type_name,
        "_id": doc_id,
        "_source": {
            "location": {
                "lat": float(doc["latitude"]),
                "lon": float(doc["longitude"])
            } if doc["latitude"] and doc["longitude"] else None,
            # Change the "location" key in the doc to "location_description".
            "location_description": doc["location"],
            # Strip out the "location field. Not strictly necessary but nice
            # to be explicit.
            **dissoc(doc, "location")
        }
    }


@click.command()
@click.argument("report_file", type=click.File('r'))
def main(report_file):

    client = elasticsearch.Elasticsearch()
    index_client = elasticsearch.client.IndicesClient(client)

    # Drop the index if it already exists; it will be replaced. This is the
    # most efficient way to delete the data from an index according to the ES
    # documentation.
    if index_client.exists(nadp_index_name):
        index_client.delete(nadp_index_name)
    
    # Create the index again.
    index_client.create(
        nadp_index_name,
        nadp_index_body
    )

    reports = DictReader(report_file)

    # Zip the reports with the report numbers.
    report_actions = map(
        nadp_bulk_action,
        reports,
        count()
    )

    bulk(client, report_actions)


if __name__ == "__main__":
    main()