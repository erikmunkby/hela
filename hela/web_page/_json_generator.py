import json
import warnings
from pathlib import Path
from hela import Catalog, BaseDataset
from typing import Dict, Any, Sequence
from collections import defaultdict


class JsonGenerator:
    _columns_dict: Dict[str, Sequence[BaseDataset]] = None

    def _build_dataset_columns_json(
        self, dataset: BaseDataset, include_samples: bool
    ) -> Sequence[Dict[str, Any]]:
        dataset_columns = dataset.columns
        columns_list = []
        # Attempt to fetch samples if boolean flag is set to true
        try:
            samples = dataset.get_samples() if include_samples else None
        except NotImplementedError:
            warnings.warn(
                f'get_samples() function not implemented for dataset {dataset.name} when include_samples=True'
            )
            samples = None
        samples = {} if samples is None else samples

        # If there are no columns in the dataset
        if dataset_columns is None:
            return []

        # Loop through the columns and build info json
        for col in dataset.columns:
            for col_info in col._describe():
                other_datasets = [
                    {'name': d.name, 'id': d._id}
                    for d in self._columns_dict[col_info.name]
                    if d._id != dataset._id
                ]
                sample = samples.get(col_info.name, None)
                sample = None if sample is None else str(sample)
                columns_list.append({
                    **col_info.__dict__,
                    'sample_data': sample,
                    'other_dataset': other_datasets
                })
        return columns_list

    def _load_rich_description(self, path_str):
        if path_str is None:
            return None
        path = Path(path_str)
        if path.exists():
            return Path(path_str).read_text()
        return f'Rich description could not be found under path {path}'

    def _build_catalog_descriptions(self,
                                    catalog: Catalog,
                                    parent: str = None,
                                    include_samples: bool = False
                                    ) -> Dict[str, Any]:
        child_list = []
        catalog_id_str = catalog.__name__ if parent is None else parent + '--' + catalog.__name__
        for cat in catalog.get_catalogs(recursive=False):
            child_list.append(self._build_catalog_descriptions(cat, catalog_id_str))

        for dataset in catalog.get_datasets(recursive=False):
            column_data = self._build_dataset_columns_json(dataset, include_samples=include_samples)
            child_list.append(
                {
                    **dataset._desc_().__dict__,
                    'rich_description': self._load_rich_description(dataset.rich_description_path),
                    'id': dataset._id,
                    'columns': column_data,
                }
            )

        return {
            **catalog._desc_().__dict__,
            'id': catalog_id_str,
            'rich_description': self._load_rich_description(catalog._rich_description_path),
            'children': child_list
        }

    def generate_docs_jsons(self, catalogs: Sequence[Catalog], include_samples: bool) -> str:
        """Generates a json string via recursively iterating through the catalog."""
        # Instantiate columns dict with columns from all datasets in all catalogs
        columns_dict = defaultdict(set)
        for catalog in catalogs:
            for col, datasets in catalog.get_columns_datasets().items():
                columns_dict[col.name].update(datasets)
        self._columns_dict = columns_dict

        json_str = json.dumps([
            self._build_catalog_descriptions(c, include_samples=include_samples)
            for c in catalogs
        ])
        return json_str
