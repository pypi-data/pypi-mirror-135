from xml.etree import ElementTree

from django.core.management import BaseCommand

from rooibos.vracore4.models import STANDARD_NAMESPACE


NAMESPACES = {'vra4': STANDARD_NAMESPACE}


def process(element):
    print(element.tag)


class Command(BaseCommand):
    help = 'Command line VRA Core 4 XML import tool'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data', '-d', dest='data_file',
            help='VRA XML file'
        )
        parser.add_argument(
            '--collection', '-c', dest='collections',
            action='append',
            help='Collection identifier'
        )

    def handle(self, *args, **kwargs):

        data_file = kwargs.get('data_file')
        collections = list(map(int, kwargs.get('collections') or list()))

        if not data_file or not collections:
            print("--collection and --data are required parameters")
            return

        with open(data_file) as data:
            root = ElementTree.fromstring(data.read())

        for child in root.findall('vra4:work', namespaces=NAMESPACES):
            process(child)
