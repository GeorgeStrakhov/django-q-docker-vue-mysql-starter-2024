import { defineStore } from 'pinia';

export const useLoadingStore = defineStore('loading', {
    // State: Defines the data to be stored, in this case, a boolean indicating if the loading screen is visible.
    state: () => ({
        isLoading: false,
        loadingMessage: 'Loading...',
    }),

    // Actions: Functions that perform operations on the state. They can be asynchronous.
    actions: {
        // Method to show the loading screen by setting isLoading to true
        showLoading(loadingMessage) {
            this.isLoading = true;
            this.loadingMessage = loadingMessage;
        },
        // Method to hide the loading screen by setting isLoading to false
        hideLoading() {
            this.isLoading = false;
            this.loadingMessage = 'Loading...';
        },
    },
});

