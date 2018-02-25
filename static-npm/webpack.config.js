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
    port: 9000,
    proxy: {
      '/puller': {
        target: 'http://localhost:5000',
        secure: false
      }
    }
  }
};
