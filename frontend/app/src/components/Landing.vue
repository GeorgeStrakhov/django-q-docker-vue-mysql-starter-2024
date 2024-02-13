<template>

    <div class="grid">
        <div class="col-12 md:col-8 md:col-offset-2">

            <Card>
            <template #content>
                <div class="text-center">
                    <h2>{{ message }}</h2>
                    <Button label="send quick api request" :loading="isShortLoading" @click="shortApiCall" />
                </div>
                <div class="text-center pt-4">
                    <Button severity="danger" label="send long api request" :loading="isLongLoading" @click="longApiCall" />
                </div>
                <div class="text-center pt-4">
                    <hr />
                    <p>Check out the <router-link :to="{name: 'NotesList'}">Notes</router-link> page for how we can fetch data from djangorestframework, protecting the route by auth.</p>
                </div>
            </template>
            </Card>

        </div>
    </div>

</template>

<script>
    import {apiGet, apiPost, showError, showSuccess} from '../helpers/api.js'
    import { eventBus } from '@/helpers/eventBus';

    export default {
        data() {
            return {
                message: 'Hello World!',
                isShortLoading: false,
                isLongLoading: false
            }
        },
        methods: {
            shortApiCall() {
                this.isShortLoading = true
                apiGet('test_data')
                    .then(response => {
                        console.log(response)
                        showSuccess(response.result.message)
                    })
                    .catch(error => {
                        showError()
                    })
                    .finally(() => {
                        this.isShortLoading = false
                    })
            },
            longApiCall() {
                this.isLongLoading = true
                eventBus.emit('show-loading', 'Please wait for something long to finish')
                apiPost('test_task', {
                    'query': 'long api call blah blah'
                })
                    .then(response => {
                        console.log(response)
                        showSuccess(response.result.message)
                    })
                    .catch(error => {
                        showError()
                    })
                    .finally(() => {
                        this.isLongLoading = false
                        eventBus.emit('hide-loading')
                    })
            }
        }
    }

</script>


