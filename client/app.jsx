import { h, render } from 'preact';

render(
  <div id="foo">
    <span>Hello, world!</span>
    <br />
    <button onClick={e => alert('Fuck yes, Preact!')}>Click Me</button>
  </div>,
  document.body,
);
