import {
  createContext,
  ReactNode,
  useCallback,
  useEffect,
  useState,
} from 'react';
import { CategoryNode, DatasetNode, TreeNode } from './types';

type SelectedItemContextParams = {
  selected: DatasetNode | CategoryNode | null;
  setSelected: (val: DatasetNode | CategoryNode | null) => void;
  setSelectedById: (id: string) => void;
  treeList: TreeNode[];
};
export const SelectedItemContext = createContext<SelectedItemContextParams>({
  selected: null,
  setSelected: () => {},
  setSelectedById: (id: string) => {},
  treeList: [],
});

const findNode = (treeList: TreeNode[], id: string): TreeNode | null => {
  for (const node of treeList) {
    if (node.id === id) {
      return node;
    }
    if (node.type === 'Catalog') {
      const targetNode = findNode(node.children || [], id);
      if (targetNode) return targetNode;
    }
  }
  return null;
};

const getSelectedIdFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('id');
  return id;
};
export const SelectedItemContextWrapper = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [selected, updateSelected] = useState<
    DatasetNode | CategoryNode | null
  >(null);
  const [treeList, setTreeList] = useState<TreeNode[]>([]);

  const init = (treeListData: TreeNode[]) => {
    const id = getSelectedIdFromUrl();
    const node = findNode(treeListData, id || '');
    if (node) {
      setSelected(node);
    } else {
      setSelected(treeListData[0]);
    }
    setTreeList(treeListData);
  };
  useEffect(() => {
    window.onpopstate = function (event) {
      const id = getSelectedIdFromUrl();
      const node = findNode(treeList, id || '');
      if (node) {
        updateSelected(node);
      }
    };
  }, [treeList]);

  useEffect(() => {
    console.log('URL', process.env.PUBLIC_URL);
    // @ts-ignore
    const treeListData = window.treeListData;
    if (treeListData) {
      init(treeListData);
    } else {
      try {
        fetch(`${process.env.PUBLIC_URL || ''}/data.json`)
          .then((a) => a.json())
          .then((data) => {
            init(data);
          });
      } catch (e) {
        alert('No data was found!');
      }
    }
  }, []);
  const setSelected = (node: DatasetNode | CategoryNode | null) => {
    try {
      window.history.pushState({}, '', `/?id=${node?.id}`);
    } catch (e) {}
    updateSelected(node);
  };
  const setSelectedById = (id: string) => {
    const node = findNode(treeList, id || '');
    if (node) {
      setSelected(node);
    }
  };
  return (
    <SelectedItemContext.Provider
      value={{ selected, setSelected, treeList, setSelectedById }}
    >
      {children}
    </SelectedItemContext.Provider>
  );
};
