const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

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
  },
  plugins: [
    new HtmlWebpackPlugin({
      title: 'MBTA Health Dashboard',
      template: './src/index.html'
    })
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          'babel-loader',
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
