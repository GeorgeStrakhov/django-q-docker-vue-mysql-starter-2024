<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2 lg:col-4 lg:col-offset-4">
            <div class="surface-card p-4 shadow-2 border-round w-full">
                <div class="text-center mb-5">
                    <div class="text-900 text-3xl font-medium mb-3">Hi there!</div>
                    <span class="text-600 font-medium line-height-3">Already have an account?</span>
                    <router-link :to="{ name: 'Login' }" class="font-medium no-underline ml-2 text-blue-500 cursor-pointer">Please sign in.</router-link>
                </div>

                <div>
                    <form @submit="onSubmit">
                        <label for="email" class="block text-900 font-medium mb-2">Email</label>
                        <InputText
                                v-model="email"
                                aria-describedby="email-help"
                                type="email"
                                id="email"
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

                        <Button type="submit" label="Sign up" class="w-full" />
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import AuthService from '@/services/authService';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';

    const schema = yup.object({
        email: yup.string().required().email().label('Email address'),
        password: yup.string().required().min(8).label('Password')
    });
    
    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [email] = defineField('email', { initialValue: '' });
    const [password] = defineField('password', { initialValue: '' });

    const onSubmit = handleSubmit(()=>{
        signup();
    });

    const signup = async () => {
        eventBus.emit('show-loading', 'Signing you up...')
        AuthService.signup(email.value, password.value)
        .then((response) => {
            eventBus.emit('toast', { severity: 'success', detail: response.message, life: 5000 });
            router.push({ name: 'VerifyEmail' });
        })
        .catch((error) => {
            eventBus.emit('toast', { severity: 'error', detail: error, life: 5000 });
        })
        .finally(() => {
            eventBus.emit('hide-loading');
        });
    };
</script>
