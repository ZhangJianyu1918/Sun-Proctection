import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createGoogleMap } from '@fawmi/vue-google-maps'


const app = createApp(App)
app.use(router)
app.use(createGoogleMap, {
    apiKey: 'AIzaSyC8ZRwMu4odONGFCfbUCIQblmDS0itPV_Y',  // 替换为您的API密钥
    libraries: ['visualization'],  // 载入热力图功能
  })
app.mount('#app')