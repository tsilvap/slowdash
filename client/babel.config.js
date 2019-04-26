const presets = [
  [
    '@babel/preset-env',
    {
      corejs: '2',
      targets: '> 0.1% in BR',
      useBuiltIns: 'usage',
    },
  ],
];

const plugins = [['@babel/plugin-transform-react-jsx', { pragma: 'h' }]];

module.exports = { presets, plugins };
