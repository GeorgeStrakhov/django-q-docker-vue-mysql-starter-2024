import { apiPost, apiGet } from '@/helpers/api';

const USER_KEY = 'user';

class AuthService {
    // Sign up a new user
    signup(email, password) {
        return apiPost('signup/', {
            email: email,
            password: password,
        });
    }

    // Sign in a user
    login(email, password) {
        console.log('logging in...');
        return apiPost('token/', {
            username: email,
            email: email,
            password: password,
            _isLogin: true, // to disable the token refresh when logging in
        }).then((response) => {
            localStorage.setItem(USER_KEY, JSON.stringify(response));
            return response;
        });
    }

    // reset password and sign in the user on success
    resetPassword(pass, uid, token) {
        return apiPost(`password_reset_confirm/${uid}/${token}/`, { password: pass })
        .then((response) => {
            localStorage.setItem(USER_KEY, JSON.stringify(response));
        }).catch((error) => {
            throw new Error(error || 'Error resetting password');
        });
    }

    // Sign out the current user
    logout() {
        localStorage.removeItem(USER_KEY);
    }

    // Get the current user from local storage
    getCurrentUser() {
        const userStr = localStorage.getItem(USER_KEY);
        if (userStr) return JSON.parse(userStr);

        return null;
    }

    // refresh token
    refreshToken() {
        const refreshToken = JSON.parse(localStorage.getItem(USER_KEY))?.refresh;
        return apiPost('token/refresh/', { refresh: refreshToken });
    }
}

export default new AuthService();
