import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primevue/resources/primevue.min.css'
import PrimeVue from 'primevue/config';


const app = createApp(App)
app.use(PrimeVue)
app.use(router)

app.mount('#app')
