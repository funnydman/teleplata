const common = require('./webpack.common.js');
const merge = require('webpack-merge');
const path = require('path');
const webpack = require('webpack');

WebpackDevServerHost = 'http://127.0.0.1:5000';

module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        contentBase: path.join(__dirname, '../templates/'),
        watchContentBase: true,
        publicPath: '/static/dist/',
        compress: true,
        port: 8080,
        hot: true,
        inline: true,
        open: true,

        proxy: {
            '/': WebpackDevServerHost,
            secure: false,
        },
        clientLogLevel: 'none',
        stats: 'errors-only'
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin()
    ],
});