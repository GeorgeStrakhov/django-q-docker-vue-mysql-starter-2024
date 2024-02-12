<template>
    <div v-if="authStore.isAuthenticated">
        <SplitButton :label="userInitials" menuButtonIcon="pi pi-cog" :model="items" />
    </div>
</template>

<script setup>
    import { computed, onMounted } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';

    const authStore = useAuthStore();

    const items = [
        {
            label: 'Logout',
            icon: 'pi pi-power-off',
            command: () => logout()
        }
    ];

    const userInitials = computed(() => {
        if (authStore.user && authStore.user.email) {
            const names = authStore.user.email.split('@')[0].split('.');
            return names.map(name => name[0].toUpperCase()).join('');
        }
        return 'user'
    });

    onMounted(() => {
        authStore.checkAuth();
    });

    const logout = async () => {

        try {
            await authStore.logout();
            eventBus.emit('toast', { severity: 'success', detail: 'Bye!', life: 1000 });
            router.push('/');
          } catch (error) {
            console.log(error)
            eventBus.emit('toast', { severity: 'error', detail: 'Couldn\'t log out :(', life: 3000 });
          }

    };
</script>
