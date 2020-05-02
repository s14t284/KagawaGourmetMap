import React from "react";
import ReactDOM from 'react-dom';

const root = document.getElementById('root');

const Root: React.FC = () => {
  return (
        <h1>{"Hello World"}</h1>
      )
}

ReactDOM.render(<Root />, root);
