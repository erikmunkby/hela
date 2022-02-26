from hela.errors import ValidationError
from hela import Catalog
from hela._catalog_class import is_dataset, is_catalog


def validate_dataset_variable_names(root_catalog: Catalog) -> True:
    """Runs a validation check to make sure field (variable) names of the catalogs
    conform with the name of their datasets.

    Args:
        root_catalog: The root catalog of your project

    Returns:
        True if all datasets were successfully validated

    Raises:
        ValidationError:    Whenever a discrepancy between field (variable) name and dataset
                            name was found
    """
    for field, obj in root_catalog.__dict__.items():
        dataset = is_dataset(obj)
        if dataset:
            if field != dataset.name:
                raise ValidationError(f'Dataset with name "{obj.name}" has field name "{field}"')
        catalog = is_catalog(obj)
        if catalog:
            validate_dataset_variable_names(catalog)
    return True


def validate_no_duplicated_columns(root_catalog: Catalog) -> True:
    """Runs a validation check to make sure there are no duplicated columns among the datasets.

    Args:
        root_catalog: The root catalog of your project

    Returns:
        True if all columns were successfully validated

    Raises:
        ValidationError:    Whenever the same columns if found in multiple datasets
                            without being referenced from store.
    """
    columns_dict = root_catalog.get_columns_datasets()
    for col, datasets in columns_dict.items():
        if len(datasets) > 1 and not col.from_store:
            raise ValidationError(
                f'Datasets {datasets} have overlapping column "{col.name}".'
                f' Consider adding column "{col.name}" to a column store and reference to store column instead.'
            )
    return True
