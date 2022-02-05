export type CategoryNode = {
  name: string;
  type: 'Catalog';
  id: string;
  description: string | null;
  rich_description: string | null;
  children?: TreeNode[];
};
export type DatasetNode = {
  name: string;
  type: 'Dataset';
  id: string;
  rich_description: string | null;
  description: string;
  columns: Column[];
};
export type Column = {
  name: string;
  data_type: string;
  description: string;
  from_store: boolean;
  other_dataset: OtherDatasetNode[] | null;
};

export type OtherDatasetNode = {
  name: string;
  id: string;
};

export type TreeNode = CategoryNode | DatasetNode;
