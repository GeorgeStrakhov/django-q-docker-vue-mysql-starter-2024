import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import { createPinia } from 'pinia';
import App from '@/App.vue'
import { router } from '@/router'
import { eventBus } from '@/helpers/eventBus';

//auth store
import { useAuthStore } from '@/stores/authStore'

//components that we will need globally
import Button from "primevue/button";
import SplitButton from 'primevue/splitbutton';
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
import FileUpload from 'primevue/fileupload';
import Paginator from 'primevue/paginator';
import ConfirmPopup from 'primevue/confirmpopup';

//services
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice';

//import 'primevue/resources/themes/lara-dark-teal/theme.css' //theme
import 'primevue/resources/themes/arya-orange/theme.css'
// import 'primevue/resources/themes/bootstrap4-light-blue/theme.css'
import 'primeflex/primeflex.css' //grid system
import 'primevue/resources/primevue.min.css' //core css
import 'primeicons/primeicons.css' //icons

import Ripple from 'primevue/ripple';

import Loading from '@/components/Loading.vue'
import Login from '@/components/Login.vue'
import Logout from '@/components/Logout.vue'
import Signup from '@/components/Signup.vue'
import EasyInput from '@/components/helpers/EasyInput.vue'
import EasyImageUpload from '@/components/helpers/EasyImageUpload.vue'

//create the app
const app = createApp(App)

//custom services
app.use(ToastService)
app.use(ConfirmationService);

//registering components that we need globally
app.component('Button', Button)
app.component('SplitButton', SplitButton)
app.component('Badge', Badge)
app.component('Divider', Divider)
app.component('RadioButton', RadioButton)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('Image', Image)
app.component('Card', Card)
app.component('InputText', InputText)
app.component('ProgressSpinner', ProgressSpinner)
app.component('Panel', Panel)
app.component('Textarea', Textarea)
app.component('Dialog', Dialog)
app.component('ConfirmPopup', ConfirmPopup)

//ripple directive
app.directive('ripple', Ripple)

//registering custom components to be reused
app.component('Loading', Loading)
app.component('Login', Login)
app.component('Logout', Logout)
app.component('Signup', Signup)
app.component('EasyInput', EasyInput)
app.component('EasyImageUpload', EasyImageUpload)

//router
app.use(router)

//store
app.use(createPinia());
const authStore = useAuthStore()
authStore.checkAuth();

app.use(PrimeVue, {ripple: true})
app.mount('#app')
