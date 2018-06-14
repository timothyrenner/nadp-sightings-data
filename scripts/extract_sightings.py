import click

from lxml import etree
from toolz import curry

def xpath(xpath_str, tree, namespaces):
    return tree.xpath(xpath_str, namespaces=namespaces)

@click.command()
@click.argument("input_file", type=click.File("r"))
def main(input_file):
    namespaces = {
        "kml": "http://www.opengis.net/kml/2.2"
    }

    dogman = etree.parse(input_file)

    kml_xpath = curry(xpath)(tree=dogman, namespaces=namespaces)

    descriptions = kml_xpath("//kml:Placemark/kml:description/text()")
    titles = kml_xpath("//kml:Placemark/kml:name/text()")
    coordinates = kml_xpath("//kml:Placemark/kml:Point/kml:coordinates/text()")

    assert len(descriptions) == len(titles)
    assert len(titles) == len(coordinates)

    # TODO: Zip together and write output.


if __name__ == "__main__":
    main()