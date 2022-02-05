import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { SelectedItemContextWrapper } from './context';

ReactDOM.render(
  <React.StrictMode>
    <SelectedItemContextWrapper>
      <App />
    </SelectedItemContextWrapper>
  </React.StrictMode>,
  document.getElementById('root'),
);
