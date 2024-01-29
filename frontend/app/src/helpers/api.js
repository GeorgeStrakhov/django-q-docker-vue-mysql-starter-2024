import axios from 'axios';

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

const showError = (t, error="something went wrong") => { //passing t as this from the component
    console.log(error);
    t.$toast.add({
        severity: 'error',
        summary: 'Sorry...',
        detail: error,
        life: 3000,
    });
};

const showSuccess = (t, message="it worked!") => { //passing t as this from the component
    t.$toast.add({
        severity: 'success',
        summary: 'Hooraay!',
        detail: message,
        life: 3000,
    });
};

export {apiPost, apiGet, showError, showSuccess};
