import { defineStore } from 'pinia'
import AuthService from '@/services/authService'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        isLoggedIn: false,
    }),
    getters: {
        getUser: (state) => state.user,
        isAuthenticated: (state) => state.isLoggedIn,
    },
    actions: {
        login(email, password) {
            return AuthService.login(email, password).then((data) => {
                this.user = data.user
                this.isLoggedIn = true
            })
        },
        logout() {
            AuthService.logout()
            this.user = null
            this.isLoggedIn = false
        },
        checkAuth() {
            const user = AuthService.getCurrentUser()
            if (user) {
                this.user = user
                this.isLoggedIn = true
            } else {
                this.user = null
                this.isLoggedIn = false
            }
        }
    }
})
