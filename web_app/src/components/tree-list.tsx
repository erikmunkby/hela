import { FiDatabase, FiFolder } from 'react-icons/fi';
import { motion } from 'framer-motion';
import { useContext, useState } from 'react';
import { SelectedItemContext } from '../context';
import { TreeNode } from '../context/types';

export const Item = ({ item }: { item: TreeNode }) => {
  const [open, setOpen] = useState(false);
  const { selected, setSelected } = useContext(SelectedItemContext);
  if (item.type === 'Catalog') {
    return (
      <li>
        <button
          onClick={() => {
            setSelected(item);
            setOpen(!open);
          }}
        >
          <FiFolder className="text-2xl mr-2" /> {item.name}{' '}
        </button>
        <motion.div
          animate={{ height: open ? 'auto' : 0 }}
          className="overflow-hidden"
        >
          {item.children && (
            <ul className="menu">
              {item.children.map((i) => (
                <Item key={i.id} item={i} />
              ))}
            </ul>
          )}
        </motion.div>
      </li>
    );
  }
  return (
    <li>
      <a onClick={() => setSelected(item)}>
        <FiDatabase className="text-2xl mr-2" /> {item.name}
      </a>
    </li>
  );
};

export const TreeList = () => {
  const { treeList } = useContext(SelectedItemContext);
  return (
    <ul className="menu pt-4">
      {treeList?.map((l, index) => (
        <Item item={l} key={index} />
      ))}
    </ul>
  );
};
