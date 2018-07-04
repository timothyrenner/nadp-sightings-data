# NADP Sightings Data

The North American Dogman Project ([NADP](https://www.northamericandogmanproject.com/)) is a group dedicated to researching Dogman, a canine cryptid that walks upright.
They have collected hundreds of sightings and host them on a map [here](https://www.northamericandogmanproject.com/encounters-.html).

This repository contains code for extracting and cleaning this dataset for further analysis.

## Setup

There is not an easy way to automate downloading the raw data, but it's a straightforward process.

1. Go to the [Encounters](https://www.northamericandogmanproject.com/encounters-.html) page on the NADP website.
2. Click the "View larger map" icon in the top right corner of the map. A page hosted by Google will open.
3. On the information panel (left side) there's a "three dot" menu expansion at the top right. Click that and select "Download KML". Be sure to select "Export to a KML file", as the script needs to load the whole thing to parse it. It's about 375k.
4. Rename that file to `north_american_dogman_sightings.kml` and put it in `data/external` in this repo.

Once you've completed these steps you're ready to extract and process the sightings.

## Extract and Process

1. Set up the conda environment.

```
conda env create -f env.yml

# source activate if you're not set up with the conda command.
conda activate nadp-sightings-data
```

2. Run make!

```
make data/processed/dogman_sightings.csv
```

You're done.
The processed file is right where the makefile says it is.