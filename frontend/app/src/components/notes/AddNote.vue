<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2">
            <div>
                <router-link :to="{name: 'NotesList'}">Back to Notes</router-link>
                <h1>Add a new Note</h1>
                <form @submit="onSubmit">
                    <EasyInput v-model="title" inputtype="inputtext" label="Note Title" :errors="errors.title" input-id="title" />
                    <EasyInput v-model="content" inputtype="textarea" label="Content" :errors="errors.content" input-id="content" />
                    <EasyImageUpload v-model="uploadedImgUrl" />
                    <Button type="submit" label="Add Note" severity="warning" icon="pi pi-check" iconPos="right" />
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, onMounted } from 'vue';
    import { apiPost, showError, showSuccess } from '@/helpers/api';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';

    const schema = yup.object({
        title: yup.string().required(),
        content: yup.string(),
    });

    const { defineField, handleSubmit, resetForm, errors } = useForm({
        validationSchema: schema,
    });

    const [title] = defineField('title');
    const [content] = defineField('content');

    const uploadedImgUrl = ref('');

    watch(uploadedImgUrl, (newValue) => {
        console.log('New image value: ', newValue);
    });

    const onSubmit = handleSubmit( async () => {
        eventBus.emit('show-loading', 'Adding a new note...');
        await addNote();
        eventBus.emit('hide-loading');
    })

    const addNote = async () => {
        const args = {
            title: title.value,
            content: content.value,
            image: uploadedImgUrl.value,
        };
        console.log('Adding a new note...');

        apiPost('rest/notes/', args)
            .then(() => {
                showSuccess('Note added successfully');
                resetForm();
                router.push({ name: 'NotesList' });
            })
            .catch((error) => {
                showError(error);
            });

    }

</script>
