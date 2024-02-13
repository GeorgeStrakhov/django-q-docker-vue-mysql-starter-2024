<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2 lg:col-4 lg:col-offset-4">
            <div class="surface-card p-4 shadow-2 border-round w-full">
                <div v-if="isEmailSent">
                    <div class="text-center mb-5">
                        <div class="text-900 text-3xl font-medium mb-3">Check your email</div>
                        <span class="text-600 font-medium line-height-3">Please check your email for a password reset link.</span>
                    </div>
                </div>
                <div v-else>
                    <div class="text-center mb-5">
                        <div class="text-900 text-3xl font-medium mb-3">Lost your password?</div>
                        <span class="text-600 font-medium line-height-3">No problem, just type your email below.</span>
                    </div>

                    <div>
                        <form @submit="onSubmit">
                                <label for="email" class="block text-900 font-medium mb-2">Email</label>
                                <InputText
                                        v-model="email"
                                        aria-describedby="email-help"
                                        type="email"
                                        class="w-full mb-1"
                                        :class="{ 'p-invalid': errors.email }"
                                        />
                                <div class="mt-0 mb-4">
                                    <small id="email-help" class="p-error">{{ errors.email }}</small>
                                </div>

                            <Button label="Reset my password" type="submit" class="w-full" />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
    import { ref } from 'vue';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';
    import { apiPost } from '@/helpers/api';

    const schema = yup.object({
        email: yup.string().required().email().label('Email address')
    });

    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [email] = defineField('email', { initialValue: '' });

    const isEmailSent = ref(false);

    const onSubmit = handleSubmit((values) => {
        sendReset();
    });

    const sendReset = () => {
        eventBus.emit('show-loading', 'Sending password reset instructions if the user exists...')

        apiPost('/password_reset/', { email: email.value, _isResetPassword: true })
        .then( (response) => {
            console.log(response)
            //eventBus.emit('toast', { severity: 'success', detail: 'If the user with such email exists, then the password reset instructions are sent to your email.', life: 5000 });
            isEmailSent.value = true;
        })
        .catch( (error) => {
            console.log(error)
            eventBus.emit('toast', { severity: 'error', detail: 'Sorry, something doesn\'t look right. Please try again.', life: 3000 });
        })
        .finally( () => {
            eventBus.emit('hide-loading');
        });

    };
</script>
