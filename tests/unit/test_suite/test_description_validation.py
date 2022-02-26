import pytest
from hela.test_suite import description_tests
from hela import Catalog, BaseDataset, Col, NestedCol
from hela.data_types import String
from hela.errors import ValidationError


@pytest.fixture
def test_catalog():
    dataset = BaseDataset(
        name='test_dataset',
        data_type='test_datatype',
        description='Test Dataset Structure.',
        columns=[
            Col('test_col', String(), 'test column one with a longer sentece'),
            Col('test_col2', String(), 'test_column_two, has additional information'),
            Col('filler_column1', String(), 'alice'),
            Col('filler_column2', String(), 'bob'),
            Col('filler_column3', String(), 'charlie'),
            NestedCol('nested', [
                Col('test_col3', String(), 'has some nested information'),
                Col('filler_column4', String(), 'david')
            ])
        ]
    )

    @Catalog.setup(description='Test Catalog Structure.')
    class TestCatalog(Catalog):
        test_dataset = dataset

    return TestCatalog


@pytest.mark.base
def test_similarty_validation(test_catalog: Catalog):
    # Base example should work fine
    assert description_tests.validate_description_similarity(test_catalog)

    # If we reduce threshold we should get avalidation hit on descriptions for dataset and catalog
    with pytest.raises(ValidationError):
        description_tests.validate_description_similarity(test_catalog, min_similarity=.4)
    # but not for below .6
    description_tests.validate_description_similarity(test_catalog, min_similarity=.6)

    # If we rename a description we should get a validation hit on descriptions with "dataset" in them
    test_catalog.test_dataset.columns.test_col2.description = 'test dataset'
    with pytest.raises(ValidationError):
        description_tests.validate_description_similarity(test_catalog)

    # Should now clash with the nested column description
    test_catalog.test_dataset.columns.test_col2.description = 'some nested information'
    with pytest.raises(ValidationError):
        description_tests.validate_no_description_duplication(test_catalog)


@pytest.mark.base
def test_no_duplication_validation(test_catalog: Catalog):
    assert description_tests.validate_no_description_duplication(test_catalog)

    # We should now get a duplication hit
    test_catalog.test_dataset.columns.test_col2.description = 'test dataset structure'
    with pytest.raises(ValidationError):
        description_tests.validate_no_description_duplication(test_catalog)

    # Adding an "e" should no longer generate a duplication hit
    test_catalog.test_dataset.columns.test_col2.description = 'test dataset structuree'
    description_tests.validate_no_description_duplication(test_catalog)
