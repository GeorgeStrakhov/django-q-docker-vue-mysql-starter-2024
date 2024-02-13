<template>
    <div class="grid">
        <div class="col-12 text-center">
            <h1>My Notes</h1>
        </div>
        <div class="col-12 md:col-6 lg:col-4" v-for="note in notes" :key="note.id">
            <Card class="w-full" style="overflow: hidden">
            <template #header>
                <div class="image-container">
                    <span v-if="note.image">
                        <img alt="note header image" :src="note.image" />
                    </span>
                </div>
            </template>
            <template #title>{{note.title}}</template>
            <template #content>
                <p class="m-0">
                    {{note.content}}
                </p>
            </template>
            <template #footer>
                <div class="flex gap-3 mt-1">
                    <router-link :to="{ name: 'Note', params: { id: note.id } }" class="p-button p-component p-button-secondary p-button-outlined w-full" ><span class="p-button-label">edit</span></router-link>
                </div>
            </template>
            </Card>
        </div>
        <div class="col-12 py-4 text-center">
            <router-link to="/add-note" class="p-button">Add a new Note</router-link>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { apiGet, showError, showSuccess } from '@/helpers/api.js'
    import { eventBus } from '@/helpers/eventBus';

    const notes = ref([]);

    onMounted(() => {
        eventBus.emit('show-loading', 'Fetching notes...');
        apiGet('rest/notes/')
                .then(response => {
                    notes.value = response;
                })
                .catch(error => showError(error))
                .finally(() => {
                    eventBus.emit('hide-loading');
                }); 
        });
</script>

<style scoped>

.image-container {
  width: 100%; 
  height: 0;
  padding-top: 56.25%; /* Aspect ratio 16:9 - adjust as needed */
  position: relative;
  background-color: pink; /* Optional: background color */
}

.image-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* Keeps the aspect ratio and fits the image within the container */
}
</style>
