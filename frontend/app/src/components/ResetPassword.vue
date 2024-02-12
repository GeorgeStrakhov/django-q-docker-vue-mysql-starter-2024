<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2 lg:col-4 lg:col-offset-4">
            <div class="surface-card p-4 shadow-2 border-round w-full">
                <div class="text-center mb-5">
                    <div class="text-900 text-3xl font-medium mb-3">Set your new Password</div>
                </div>

                <div>
                    <form @submit="onSubmit">
                        <label for="password" class="block text-900 font-medium mb-2">Password</label>
                        <InputText
                                v-model="password"
                                id="password"
                                aria-describedby="password-help"
                                type="password"
                                @keyup.enter="onSubmit"
                                class="w-full mb-1"
                                :class="{ 'p-invalid': errors.email }"
                                />
                        <div class="mt-0 mb-4">
                            <small id="password-help" class="p-error">{{ errors.password }}</small>
                        </div>

                        <Button label="Save" class="w-full" type="submit" />
                    </form>
                </div>
            </div>
        </div>
    </div>

</template>


<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import AuthService from '@/services/authService';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';
    import { useRoute } from 'vue-router';

    const schema = yup.object({
        password: yup.string().required().min(8).label('Password')
    });

    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [password] = defineField('password', { initialValue: '' });

    const authStore = useAuthStore();
    const route = useRoute();

    const onSubmit = handleSubmit(async () => {
        await save();
    });

    const save = async () => {
        eventBus.emit('show-loading', 'Saving your new password...')
        AuthService.resetPassword(password.value, route.params.uid, route.params.token).then((response) => {
            authStore.checkAuth(); //set the user in the store
            eventBus.emit('toast', { severity: 'success', detail: 'You are all set!', life: 3000 });
            router.push('/');
        }).catch((error) => {
            console.error(error);
            eventBus.emit('toast', { severity: 'error', detail: error, life: 5000 });
        }).finally(() => {
            eventBus.emit('hide-loading');
        });
    };

</script>
