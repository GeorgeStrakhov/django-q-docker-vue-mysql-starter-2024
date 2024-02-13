<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2">
            <div>
                <router-link :to="{name: 'NotesList'}">Back to Notes</router-link>
                <h1>Edit your note</h1>
                <div v-if="loaded">
                    <form @submit="onSubmit">
                        <EasyInput v-model="title" inputtype="inputtext" label="Note Title" :errors="errors.title" input-id="title" />
                        <EasyInput v-model="content" inputtype="textarea" label="Content" :errors="errors.content" input-id="content" />
                        <EasyImageUpload v-model="uploadedImgUrl" />
                        <Button type="submit" label="Save" severity="warning" icon="pi pi-check" iconPos="right" />
                    </form>
                    <div class="mx-0 my-4">
                        <hr />
                    </div>
                    <Button type="button" label="Delete" class="p-button-outlined" severity="danger" @click="confirmDelete($event)" icon="pi pi-trash" iconPos="right" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { apiGet, apiPut, apiDelete, showError, showSuccess } from '@/helpers/api';
    import { useConfirm } from 'primevue/useconfirm';
    import * as yup from 'yup';
    import { useField, useForm } from 'vee-validate';
    import { eventBus } from '@/helpers/eventBus';
    import { router } from '@/router';

    const confirm = useConfirm();

    const loaded = ref(false);

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

    onMounted(() => {
        eventBus.emit('show-loading', 'Loading note...');
        loadNote();
    });

    const loadNote = () => {
        const noteId = router.currentRoute.value.params.id;
        apiGet(`rest/notes/${noteId}/`)
            .then((response) => {
                loaded.value = true;
                title.value = response.title;
                content.value = response.content;
                uploadedImgUrl.value = response.image;
            })
            .catch((error) => {
                showError(error);
                //if the note is not found, redirect to the notes list
                router.push({ name: 'NotesList' });
            })
            .finally(() => {
                eventBus.emit('hide-loading');
            });
    }

    //confirm delete
    const confirmDelete = (event) => {
        confirm.require({
            target: event.currentTarget,
            message: 'Sure?',
            icon: 'pi pi-exclamation-triangle',
            rejectClass: 'p-button-secondary p-button-outlined p-button-sm',
            acceptClass: 'p-button-sm p-button-danger p-button-outlined',
            rejectLabel: 'Cancel',
            acceptLabel: 'Delete',
            accept: () => {
                console.log('Deleting the note...');
                deleteNote()
            }
        });
    }

    const deleteNote = () => {
        const noteId = router.currentRoute.value.params.id;
        apiDelete(`rest/notes/${noteId}/`)
            .then((response) => {
                showSuccess('Note deleted successfully');
                router.push({ name: 'NotesList' });
            })
            .catch((error) => {
                showError(error);
                //if the note is not found, redirect to the notes list
                router.push({ name: 'NotesList' });
            })
            .finally(() => {
                eventBus.emit('hide-loading');
            });
    }

    const onSubmit = handleSubmit( async () => {
        eventBus.emit('show-loading', 'Saving your note...');
        await saveNote();
        eventBus.emit('hide-loading');
    })

    const saveNote = async () => {
        const noteId = router.currentRoute.value.params.id;
        const args = {
            title: title.value,
            content: content.value,
            image: uploadedImgUrl.value,
        };
        console.log('Adding a new note...');

        apiPut(`rest/notes/${noteId}/`, args)
            .then(() => {
                showSuccess('Note saved successfully');
                resetForm();
                router.push({ name: 'NotesList' });
            })
            .catch((error) => {
                showError(error);
            });

    }

</script>
