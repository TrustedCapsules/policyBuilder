module.exports = {
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
	devtool: 'eval-source-map',
  devServer: {
    contentBase: './html',
    publicPath: '/dist'
  }
};
