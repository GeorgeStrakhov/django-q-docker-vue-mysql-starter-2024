<template>
    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2">
            <div>
                <div v-if="isLoading">
                    <Loading />
                    <p class="text-center">Loading the notes from the api...</p>
                </div>
                <div v-else>
                    <h1>Notes</h1>
                    <ul>
                        <li v-for="note in notes" :key="note.id">
                            {{ note.title }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { apiGet, showError, showSuccess } from '../helpers/api.js'
    export default {
        data() {
            return {
                notes: [],
                isLoading: true
            };
        },
        mounted() {
            this.isLoading = true;
            apiGet('rest/notes')
                .then(response => {
                    this.notes = response;
                    if (this.notes.length === 0) {
                        showError('No notes found in the database. Please add some via the admin at /api/admin/.');
                    }
                })
                .catch(error => showError(error))
                .finally(() => {
                    this.isLoading = false;
                });
        }
    };
</script>

