import { ReactNode, useContext } from 'react';
import { FiDatabase, FiFolder } from 'react-icons/fi';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { SelectedItemContext } from '../context';

type ContainerProps = {
  children: ReactNode;
};
const Container = ({ children }: ContainerProps) => {
  return (
    <div className="p-4 md:p-10 min-h-screen">
      <div className="card lg:card-side card-bordered bg-base-100 ">
        <div className="card-body">{children}</div>
      </div>
    </div>
  );
};

export const ItemView = () => {
  const { selected, setSelectedById } = useContext(SelectedItemContext);

  if (selected?.type === 'Catalog') {
    return (
      <Container>
        <h2 className="card-title flex items-center">
          <FiFolder className="mr-2" /> {selected.name}
        </h2>
        {selected.rich_description && (
          <article className="prose prose-md ">
            <ReactMarkdown
              children={selected.rich_description}
              remarkPlugins={[remarkGfm]}
            />
          </article>
        )}
      </Container>
    );
  }
  if (selected?.type === 'Dataset') {
    return (
      <Container>
        <h2 className="card-title flex items-center">
          <FiDatabase className="mr-2" />
          {selected.name}
        </h2>
        <p className="py-2 pb-4">{selected.description}</p>
        {selected.rich_description && (
          <article className="prose prose-md ">
            <ReactMarkdown
              children={selected.rich_description}
              remarkPlugins={[remarkGfm]}
            />
          </article>
        )}
        <div className="overflow-x-auto mt-6">
          <div id="data-grid">
            <div className="uppercase text-md font-bold bg-base-200 flex items-center rounded-l-lg">
              Name
            </div>
            <div className="uppercase text-md font-bold bg-base-200 flex items-center">
              Data_type
            </div>
            <div className="uppercase text-md font-bold bg-base-200 flex items-center">
              Description
            </div>
            <div className="uppercase text-md font-bold bg-base-200 flex items-center rounded-r-lg">
              Also exist in
            </div>
            {selected?.columns.map((p) => (
              <>
                <div>{p.name}</div>
                <div>{p.data_type}</div>
                <div>{p.description}</div>
                <div>
                  {p.other_dataset?.map((otherDataset) => (
                    <button
                      id={otherDataset.id}
                      className="link pl-2 link-accent"
                      onClick={() => setSelectedById(otherDataset.id)}
                    >
                      {otherDataset.name}
                    </button>
                  ))}
                </div>
              </>
            ))}
          </div>
        </div>
      </Container>
    );
  }
  return null;
};
