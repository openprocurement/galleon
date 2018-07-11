import pytest
import os.path
import yaml
import json
from jsonschema import RefResolver

from galleon import Mapper

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, 'data/extended.yaml')) as file:
    MAPPING = yaml.load(file)

with open(os.path.join(here, 'data/extended.json')) as file:
    SCHEMA = yaml.load(file)

TENDER = {}
RESULT = {
    '$schema': 'https://raw.githubusercontent.com/openprocurement/openprocurement-ocds-mapping/master/schemas/1.1-extended-schema.json',
    'ocid': 'ocds-be6bcu',
    'language': 'uk',
    'initiationType': ['tender']
}



class TestMapperExtensions(object):
    params = {
        'test_ext': [
            {
                'data': TENDER,
                'result': RESULT
            }
        ]
    }

    mapper = Mapper(
        MAPPING, RefResolver.from_schema(SCHEMA)
    )

    @pytest.mark.skip
    def test_ext(self, data, result):
        # assert self.mapper.apply(data) == result

        data['bids'] = [
            {
                'id': 'id',
                'status': 'active'
            },
            {
                'id': 'id',
                'status': 'invalid.pre-qualification'
            }
        ]
        assert self.mapper.apply(data)['bids']['details'] == [
            {'id': 'id', 'status': 'valid'},
            {'id': 'id', 'status': 'disqualified'}
        ]

        data['shortlistedFirms'] = [
            {
                'name': 'name'
            }
        ]
        assert (self.mapper.apply(data)['tender']['shortlistedFirms'] ==
            data['shortlistedFirms'])

        data['cancellations'] = [
            {
                'cancellationOf': 'tender'
            }
        ]
        assert self.mapper.apply(data)['tender']['pendingCancellation']

        data['cancellations'].append(
            {
                'cancellationOf': 'lot',
                'relatedLot': 'lot_id'
            }
        )
        data['lots'] = [
            {
                'id': 'lot_id'
            },
            {
                'id': 'spam'
            }
        ]
        for lot in self.mapper.apply(data)['tender']['lots']:
            if lot['id'] == 'lot_id' and lot['pendingCancellation']:
                assert 1
                break
        else:
            assert 0

        data['guarantee'] = {
            'amount': 1.5,
            'currency': 'UAH',
        }
        data['lots'][0]['guarantee'] = data['guarantee']
        assert self.mapper.apply(data)['tender']['guarantee'] == data['guarantee']
        assert self.mapper.apply(data)['tender']['lots'][0]['guarantee'] == data['guarantee']

        data['procuringEntity'] = {
            'identifier': {
                'id': 'id'
            }
        }
        assert self.mapper.apply(data)['parties'] == [
            {'identifier': {'id': 'id'}, 'roles': ['procuringEntity']}
        ]

