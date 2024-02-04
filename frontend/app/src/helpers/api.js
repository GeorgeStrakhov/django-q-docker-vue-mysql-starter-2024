import axios from 'axios';
import emitter from '@/helpers/eventBus';
import { toRaw } from 'vue';

//poll freq
const pollFreq = 500; //every half a second

// Base Axios instance
const api = axios.create({
    baseURL: '/api',
});

// Function to poll the task status
const pollTask = async (taskId) => {
    let result;
    try {
        do {
            const response = await api.post('/shared_services/check_task', {
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
        if (response.data.task_id) {
            // If response contains task_id, it's a long-running task
            return await pollTask(response.data.task_id);
        }
        // For instant tasks
        return response.data;
    } catch (error) {
        throw new Error('API request failed');
    }
};

const apiPost = (url, data) => makeRequest('post', url, data);
const apiGet = (url) => makeRequest('get', url);


const showError = (error="something went wrong") => {
    console.log(error);
    const payload = {severity: 'error', summary: 'Sorry...', detail: error, life: 3000};
    emitter.emit('toast', payload);
};

const showSuccess = (message="it worked!") => {
    const payload = {severity: 'success', summary: 'Hooraay!', detail: message, life: 3000};
    emitter.emit('toast', payload);
};

export {apiPost, apiGet, showError, showSuccess};
