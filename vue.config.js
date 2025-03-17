const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  devServer: {
    proxy: 'https://udax33y435.execute-api.us-east-1.amazonaws.com',
  },
};