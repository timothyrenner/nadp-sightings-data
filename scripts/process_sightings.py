import click
import csv
import re

from toolz import get, thread_first
from datetime import date

STATE_ABBREVS = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Washington DC": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}

MYD_RE = re.compile(r"(\d\d?)[-/](\d\d?)[-/](\d{4})")

HTML_RE = re.compile(r"<[^>]*>")


def process_location(location):
    return thread_first(
        location,
        # Remove leading and trailing spaces.
        lambda x: x.strip(),
        # Some of the locations have digits at the end if there are
        # duplicates in the same city/county.
        lambda x: x[:-1] if x[-1].isdigit() else x,
        # After removing the digits, strip spaces one more time (only needs
        # to be at the end since the beginning wasn't changed).
        lambda x: x.rstrip()
    )


def extract_full_date(description):
    matched_description = MYD_RE.search(description)

    if matched_description:
        return date(
            month=int(matched_description[1]),
            day=int(matched_description[2]),
            year=int(matched_description[3])
        )
    else:
        return None


def strip_html_tags(description):
    return HTML_RE.sub("\n", description)

@click.command()
@click.argument("input_file", type=click.File("r"))
@click.option(
    "--output-file", "-o",
    type=click.File("w"),
    default="data/processed/dogman_sightings.csv"
)
def main(input_file, output_file):
    reader = csv.DictReader(input_file)

    writer = csv.DictWriter(output_file, fieldnames=[
        "state",
        "state_abbrev",
        "location",
        "longitude",
        "latitude",
        "date",
        "description"
    ])
    writer.writeheader()

    # Diagnostic counters.
    num_sightings = 0
    no_dates = 0

    for row in reader:

        num_sightings += 1

        # Extract the latitude and longitude.
        longitude, latitude, _ = row["coordinates"].split(",")

        # Extract the state and county.
        state, location = row["title"].split(" - ")

        sighting_date = extract_full_date(row["description"])
        if sighting_date:
            sighting_date = sighting_date.strftime("%Y-%m-%d")
        else:
            no_dates += 1

        detagged_description = strip_html_tags(row["description"])

        writer.writerow({
            "state": state.strip(),
            "state_abbrev": get(state.strip(), STATE_ABBREVS, state.strip()),
            "location": process_location(location),
            "description": detagged_description,
            "longitude": float(longitude.strip()),
            "latitude": float(latitude.strip()),
            "date": sighting_date
        })
    

if __name__ == "__main__":
    main()