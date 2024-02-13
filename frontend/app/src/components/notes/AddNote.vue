<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2">
            <div>
                <router-link to="/notes">Back to Notes</router-link>
                <h1>Add a new Note</h1>
                <form @submit="onSubmit">
                    <EasyInput v-model="title" inputtype="inputtext" label="Note Title" :errors="errors.title" input-id="title" />
                    <EasyInput v-model="content" inputtype="textarea" label="Content" :errors="errors.content" input-id="content" />
                    <EasyImageUpload v-model:imgUrl="uploadedImgUrl" />
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { apiPost, showError, showSuccess } from '@/helpers/api';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import { eventBus } from '@/helpers/eventBus';

    const schema = yup.object({
        title: yup.string().required(),
        content: yup.string(),
    });

    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [title] = defineField('title');
    const [content] = defineField('content');

    const uploadedImgUrl = ref(null);

    const onSubmit = handleSubmit( async () => {
        eventBus.emit('show-loading', 'Adding a new note...');
        await addNote();
        eventBus.emit('hide-loading');
    })

    const addNote = async () => {
        console.log('Adding a new note...');
    }

</script>
