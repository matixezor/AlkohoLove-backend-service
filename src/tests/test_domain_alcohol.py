from pytest import mark

from src.domain.alcohol import AlcoholCreate, AlcoholUpdate


@mark.parametrize(
    'srm,expected_srm',
    [
        ('40', 40.0),
        ('40.0', 40.0),
        ('asd', 'asd'),
        (None, None),
        (40, 40)
    ],
)
def test_alcohol_update_root_validator(srm: str, expected_srm: any):
    alcohol_update = AlcoholUpdate(
        name='test_name',
        srm=srm
    )
    assert alcohol_update.dict()['srm'] == expected_srm


@mark.parametrize(
    'srm,expected_srm',
    [
        ('40', 40.0),
        ('40.0', 40.0),
        ('asd', 'asd'),
        (None, None),
        (40, 40)
    ],
)
def test_alcohol_create_root_validator(srm: str, expected_srm: any):
    alcohol_create = AlcoholCreate(
        name='test_name',
        kind='test_kind',
        type='test_type',
        alcohol_by_volume=40.0,
        description='test_description',
        color='test_color',
        manufacturer='test_manufacturer',
        country='test_country',
        food=[],
        finish=[],
        aroma=[],
        taste=[],
        barcode=['123456789'],
        keywords=[],
        srm=srm
    )
    assert alcohol_create.dict()['srm'] == expected_srm
