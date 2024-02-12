<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2 lg:col-4 lg:col-offset-4">
            <div class="surface-card p-4 shadow-2 border-round w-full">
                <div class="text-center mb-5">
                    <div class="text-900 text-3xl font-medium mb-3">Welcome Back</div>
                    <span class="text-600 font-medium line-height-3">Don't have an account?</span>
                    <router-link :to="{ name: 'Signup' }" class="font-medium no-underline ml-2 text-blue-500 cursor-pointer">Create today!</router-link>
                </div>

                <div>
                    <form @submit="onSubmit">
                        <label for="email" class="block text-900 font-medium mb-2">Email</label>
                        <InputText
                                v-model="email"
                                aria-describedby="email-help"
                                id="email"
                                type="email"
                                class="w-full mb-1"
                                :class="{ 'p-invalid': errors.email }"
                                />

                        <div class="mt-0 mb-4">
                            <small id="email-help" class="p-error">{{ errors.email }}</small>
                        </div>
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

                        <div class="flex align-items-center justify-content-between mb-6">
                            <router-link :to="{ name: 'ForgotPassword' }" class="font-medium no-underline text-blue-500 text-right cursor-pointer">Forgot password?</router-link>
                        </div>

                        <Button type="submit" label="Log In" class="w-full" />
                    </form>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useAuthStore } from '@/stores/authStore';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';
    import { useRoute } from 'vue-router';

    const schema = yup.object({
        email: yup.string().required().email().label('Email address'),
        password: yup.string().required().label('Password')
    });
    
    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [email] = defineField('email', { initialValue: '' });
    const [password] = defineField('password', { initialValue: '' });

    const authStore = useAuthStore();
    const route = useRoute();

    onMounted(() => {
        authStore.checkAuth();
        if (authStore.isAuthenticated) {
            router.push('/');
        }
    });

    const onSubmit = handleSubmit( async ()=>{
        await login();
    });

    const login = async () => {
        eventBus.emit('show-loading', 'Logging in...')
        authStore.login(email.value, password.value)
        .then(() => {
            if (route.query && route.query.redirect) {
                router.push(route.query.redirect.toString());
            } else {
                router.push('/');
            }
            eventBus.emit('toast', { severity: 'success', detail: 'You are in!', life: 3000 });
        })
        .catch((error) => {
            eventBus.emit('toast', { severity: 'error', detail: error, life: 3000 });
        })
        .finally(() => {
            eventBus.emit('hide-loading');
        });
    };
</script>
