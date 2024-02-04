import { createRouter, createWebHistory } from 'vue-router'


//app components
import Landing from './components/Landing.vue'
import NotFound from './components/NotFound.vue'
import Notes from './components/Notes.vue'

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

export { router }
