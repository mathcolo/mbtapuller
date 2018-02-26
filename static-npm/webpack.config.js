const path = require('path');

module.exports = {
  entry: ['./src/index.js'],
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  devServer: {
    publicPath: "/",
    contentBase: "./dist",
    inline: true,
    hot: true,
    host: '0.0.0.0',
    port: 9000,
    proxy: {
      '/puller': {
        target: 'http://localhost:5000',
        secure: false
      }
    }
  }
};
