data/raw/dogman_sightings.csv: data/external/north_american_dogman_sightings.kml
	python scripts/extract_sightings.py \
		data/external/north_american_dogman_sightings.kml \
		--output-file data/raw/dogman_sightings.csv

data/processed/dogman_sightings.csv: data/raw/dogman_sightings.csv
	python scripts/process_sightings.py \
		data/raw/dogman_sightings.csv \
		--output-file data/processed/dogman_sightings.csv
