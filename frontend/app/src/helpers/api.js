import axios from 'axios';
import { eventBus } from '@/helpers/eventBus';
import AuthService from '@/services/authService';
import { router } from '@/router';

//poll freq
const pollFreq = 500; //every half a second

// Base Axios instance
const api = axios.create({
    baseURL: '/api',
    headers: {
        "Content-type": "application/json"
    },
    withCredentials: true
});

// Add a request interceptors for CSRF
api.interceptors.request.use((config) => {
    if (config.method === 'post' || config.method === 'put') {
        const csrfCookieName = 'csrftoken'; // Adjust the cookie name as per your Django configuration
        const csrfToken = getCookie(csrfCookieName);
        if (csrfToken) {
            config.headers['X-CSRFToken'] = csrfToken;
        }
    }
    return config;
});

// Function to get a cookie by name
export function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split?.(';')?.shift()?.trim(); // Trim whitespace
    }
};

// Add a request interceptor for JWT
api.interceptors.request.use(
    config => {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.access) {
            config.headers["Authorization"] = 'Bearer ' + user.access;
        }
        return config;
    },
    error => {
        Promise.reject(error)
    });

// Add a response interceptor for JWT
api.interceptors.response.use((response) => {
    return response
}, async function (error) {
    const originalRequest = error.config;

    let requestData = {};
    if (originalRequest.data) {
        requestData = JSON.parse(originalRequest.data);
    }

    //prevent infinite loop
    if (error.response.status === 401 && originalRequest.url.includes('token/refresh/')) {
        AuthService.logout();
        router.push('/login');
        return Promise.reject('Your session has expired. Please log in again.');
    }
    //if the error is 401 and the request has not been retried - this is for refreshing the token
    if (error.response.status === 401 && !requestData._isLogin && !requestData._isSignup && !requestData._isResetPassword) { //disable for login and signup
        //not retrying - then we just need to refresh token
        if(!originalRequest._retry) {
            console.log('access token expired, refreshing...')
            originalRequest._retry = true;
            const data = await AuthService.refreshToken();
            if (data.access) {
                localStorage.setItem('user', JSON.stringify(data));
                api.defaults.headers.common['Authorization'] = 'Bearer ' + data.access;
                return api(originalRequest);
            }
        }
    }

    // Do something with validation errors to show them to the user
    if (error.response && error.response.status === 400) {
        console.log(error);
        let messages = [];
        const errors = error.response.data;
        if (errors && typeof errors === 'object') {
            for (const field in errors) {
                if(errors[field] instanceof Array) {
                    // Assuming each field's errors are an array
                    errors[field].forEach((message) => {
                        messages.push(`${field}: ${message}`);
                    });
                } else {
                    messages.push(`${field}: ${errors[field]}`);
                }
            }
        }
        // Combine messages into a single string, or handle as needed
        const userFriendlyErrors = messages.join('. ');
        return Promise.reject(userFriendlyErrors);
    }
    return Promise.reject(error);
});

// Function to poll the task status
const pollTask = async (taskId) => {
    let result;
    try {
        do {
            const response = await api.post('/tasks/check_task', {
                task_id: taskId
            });
            result = response.data;
            if (!result.completed) {
                await new Promise(resolve => setTimeout(resolve, pollFreq));
            }
        } while (!result.completed);
    } catch (error) {
        throw new Error('Error polling task status');
    }
    return result;
};

// Function to handle API requests
const makeRequest = async (method, url, data = null) => {
    try {
        const response = await api[method](url, data);
        if (response.data && response.data.task_id) {
            // If response contains task_id, it's a long-running task
            return await pollTask(response.data.task_id);
        }
        // For instant tasks
        return response.data || response;
    } catch (error) {
        let err = error || error.message
        if (error.response && error.response.data && error.response.data.error) {
            err = error.response.data.error;
        }
        if (error.response && error.response.data && error.response.data.detail) {
            err = error.response.data.detail;
        }
        throw new Error(err);
    }
};

const apiPost = (url, data) => makeRequest('post', url, data);
const apiPut = (url, data) => makeRequest('put', url, data);
const apiGet = (url) => makeRequest('get', url);
const apiDelete = (url) => makeRequest('delete', url);

const showError = (error="something went wrong") => {
    console.log(error);
    const payload = {severity: 'error', summary: 'Sorry...', detail: error, life: 3000};
    eventBus.emit('toast', payload);
};

const showSuccess = (message="it worked!") => {
    const payload = {severity: 'success', summary: 'Hooraay!', detail: message, life: 3000};
    eventBus.emit('toast', payload);
};

export { apiPost, apiGet, apiPut, apiDelete, showError, showSuccess };
