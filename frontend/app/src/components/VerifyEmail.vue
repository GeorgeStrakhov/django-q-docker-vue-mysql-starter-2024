<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2 lg:col-4 lg:col-offset-4">
            <div class="surface-card p-4 shadow-2 border-round w-full">
                <div class="text-center mb-5">
                    <div class="text-900 text-3xl font-medium mb-3">Verify your email</div>
                    <span class="text-600 font-medium line-height-3">Please check your email for a verification link.</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { onMounted } from 'vue';
    import { eventBus } from '@/helpers/eventBus';
    import { apiGet, apiPost } from '@/helpers/api';
    import { router } from '@/router';
    import { useAuthStore } from '@/stores/authStore';

    const authStore = useAuthStore();

    const props = defineProps({
        uid: String,
        token: String
    });

    const verifyEmail = () => {
        if (!props.uid || !props.token) {
            return;
        }
        apiGet(`/verify/${props.uid}/${props.token}/`)
        .then(response => {
            // Handle successful verification
            localStorage.setItem('user', JSON.stringify(response));
            // Update authentication state and redirect user
            authStore.checkAuth();
            router.push('/');
        })
        .catch(error => {
            console.error(error);
            eventBus.emit('toast', { severity: 'error', detail: error, life: 5000 });
        });
    };

    onMounted(() => {
        verifyEmail();
    });

</script>
