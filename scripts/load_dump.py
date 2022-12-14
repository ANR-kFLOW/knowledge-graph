import os
from os import path
import requests
import argparse

from db_utils import base, get_auth

BASE_GRAPH = 'http://kflow.eurecom.fr'

ROOT = './dump'
INTERNAL_ROOT = '/opt/graphdb/home/graphdb-import'

C_TYPE = {
    'rdf': 'application/rdf+xml',
    'owl': 'text/turtle',
    'ttl': 'text/turtle'
}


def load_dump(name):
    main_graph = path.join(BASE_GRAPH, name)
    folder = path.join(ROOT, name)

    # clear graph
    headers = {'Authorization': get_auth()}
    params = (('graph', main_graph),)

    print('Deleting graph...')
    response = requests.delete(f'{base}/repositories/kflow/rdf-graphs/service',
                               headers=headers, params=params)
    if response.status_code != 204:
        print(response.status_code)
        print(response.content)
        return

    print('Uploading new resources...')
    # upload new resources
    for filename in os.listdir(folder):
        if not '.' in filename or filename.startswith('.'):
            continue
        print(filename)
        name, ext = filename.rsplit('.', 2)
        if ext in C_TYPE:
            print('- ' + name)
            headers['Content-Type'] = C_TYPE[ext]

            with open(path.join(folder, filename), 'r', encoding='utf-8') as f:
                data = f.read()

            response = requests.post(f'{base}/repositories/kflow/rdf-graphs/service',
                                     headers=headers, params=params, data=data.encode('utf-8'))
            if response.status_code != 204:
                print(response.status_code)
                print(response.content)

        else:
            continue
    print('completed')


parser = argparse.ArgumentParser(description='Load dump in a graph.')
parser.add_argument('name')
args = parser.parse_args()
load_dump(args.name)
