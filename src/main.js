import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import { Chart, registerables } from 'chart.js';
import { Line } from 'vue-chartjs';
// import '@fortawesome/fontawesome-free/css/all.min.css';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
// import vueCrypt from 'vue-crypt'

library.add(fas);
Chart.register(...registerables);
const app = createApp(App)
// app.use(vueCrypt)
app.component('font-awesome-icon', FontAwesomeIcon);
app.use(router)
app.component('LineChart', Line);
app.mount('#app')