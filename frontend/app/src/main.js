import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

//components that we will need globally
import Button from "primevue/button";
import Image from "primevue/image";
import Card from "primevue/card";
import Badge from "primevue/badge";
import Divider from "primevue/divider";
import InputText from "primevue/inputtext";
import Textarea from 'primevue/textarea';
import ProgressSpinner from 'primevue/progressspinner';
import Panel from 'primevue/panel';
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';
import RadioButton from 'primevue/radiobutton';

//services
import ToastService from 'primevue/toastservice';

//import 'primevue/resources/themes/lara-dark-teal/theme.css' //theme
import 'primevue/resources/themes/arya-orange/theme.css'
// import 'primevue/resources/themes/bootstrap4-light-blue/theme.css'
import 'primeflex/primeflex.css' //grid system
import 'primevue/resources/primevue.min.css' //core css

import Ripple from 'primevue/ripple';

//app components
import Landing from './components/Landing.vue'
import NotFound from './components/NotFound.vue'

import Loading from './components/Loading.vue'
import Notes from './components/Notes.vue'

//create the app
const app = createApp(App)

//custom services
app.use(ToastService)

//registering components that we need globally
app.component('Button', Button)
app.component('Badge', Badge)
app.component('Divider', Divider)
app.component('RadioButton', RadioButton)
app.component('Toast', Toast)
app.component('Image', Image)
app.component('Card', Card)
app.component('InputText', InputText)
app.component('ProgressSpinner', ProgressSpinner)
app.component('Panel', Panel)
app.component('Textarea', Textarea)
app.component('Dialog', Dialog)
app.directive('ripple', Ripple)

//registering custom components to be reused
app.component('Loading', Loading)

//router
const routes = [
    { path: '/', name: 'Landing', component: Landing },
    { path: '/notes', name: 'Notes', component: Notes },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

app.use(router)

app.use(PrimeVue, {ripple: true})
app.mount('#app')
