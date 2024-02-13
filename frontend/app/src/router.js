import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

//app components
import Landing from './components/Landing.vue'
import NotFound from './components/NotFound.vue'
import NotesList from './components/notes/NotesList.vue'
import Note from './components/notes/Note.vue'
import AddNote from './components/notes/AddNote.vue'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import VerifyEmail from './components/VerifyEmail.vue'
import ForgotPassword from './components/ForgotPassword.vue'
import ResetPassword from './components/ResetPassword.vue'

//router
const routes = [
    { path: '/', name: 'Landing', component: Landing },
    { path: '/login', name: 'Login', component: Login },
    { path: '/signup', name: 'Signup', component: Signup },
    { path: '/verify/:uid?/:token?', name: 'VerifyEmail', component: VerifyEmail, props: true },
    { path: '/forgotpassword', name: 'ForgotPassword', component: ForgotPassword },
    { path: '/resetpassword/:uid/:token', name: 'ResetPassword', component: ResetPassword, props: true },
    { path: '/notes', name: 'NotesList', component: NotesList, meta: { requiresAuth: true } },
    { path: '/notes/:id', name: 'Note', component: Note, meta: { requiresAuth: true }, props: true },
    { path: '/add-note', name: 'AddNote', component: AddNote, meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.isLoggedIn) {
        next({ path: '/login', query: { redirect: to.fullPath } });
    } else {
        next();
    }
});


export { router }
