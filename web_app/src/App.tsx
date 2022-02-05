import React, { useEffect, useState } from 'react';
import { ItemView } from './components/item-view';
import { TreeList } from './components/tree-list';

const themes = [
  'light',
  'dark',
  'cupcake',
  'bumblebee',
  'emerald',
  'corporate',
  'synthwave',
  'retro',
  'cyberpunk',
  'valentine',
  'halloween',
  'garden',
  'forest',
  'aqua',
  'lofi',
  'pastel',
  'fantasy',
  'wireframe',
  'black',
  'luxury',
  'dracula',
  'cmyk',
];
function App() {
  const [theme, setTheme] = useState('dark');
  useEffect(() => {
    const element = document.getElementById('html');
    element?.setAttribute('data-theme', theme);
  }, [theme]);
  return (
    <div>
      <div className="rounded-lg shadow bg-base-100 drawer drawer-mobile h-screen">
        <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />

        <div className="flex flex-col drawer-content bg-base-200 pb-8">
          <div className="flex justify-between lg:justify-end p-2  border-b border-base-300 bg-base-100 h-16 ">
            <label
              htmlFor="my-drawer-2"
              className="mb-4 btn btn-primary drawer-button lg:hidden"
            >
              open menu
            </label>
            <select
              className="select select-bordered w-[200px]"
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
            >
              {themes.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>
          <ItemView />
        </div>
        <div className="drawer-side border-r border-base-300 lg:min-w-[300px] bg-base-100 ">
          <label htmlFor="my-drawer-2" className="drawer-overlay"></label>
          <div className="bg-base-100 max-w-[90%] md:max-w-full">
            <div className="h-16 border-base-300 flex justify-center items-center border-b border-b-base-300">
              Dashboard
            </div>
            <TreeList />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
