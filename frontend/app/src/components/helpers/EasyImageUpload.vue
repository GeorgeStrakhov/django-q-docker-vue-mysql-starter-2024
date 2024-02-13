<template>
    <div class="pb-4">
        <div v-if="imgUrl">
            <div class="image-container">
                <img :src="imgUrl" alt="Uploaded image" width="200" />
                <button class="delete-icon" @click="handleClearImage">X</button>
            </div>
        </div>
        <div v-else>
            <FileUpload
                mode="basic"
                name="img_upload"
                url="/api/img_upload/"
                @beforeUpload="showLoading"
                @upload="onUpload"
                accept="image/*"
                :fileLimit="1"
                :maxFileSize="maxFileSize"
                :auto="true" />
        </div>
    </div>
</template>

<script setup>
    import { ref, watch } from 'vue';
    import FileUpload from 'primevue/fileupload';
    import { eventBus } from '@/helpers/eventBus';
    import { defineProps, defineEmits } from 'vue';

    const props = defineProps({
        modelValue: String,
        maxFileSize: {
            type: Number,
            default: 2000000, // 2MB default max file size
        },
    });

    const emit = defineEmits(['update:modelValue']);

    const imgUrl = ref(props.modelValue);

    // Ensure imgUrl is reactive to parent changes
    watch(() => props.modelValue, (newValue) => {
        imgUrl.value = newValue;
    });

    // When imgUrl changes internally, emit the change
    watch(imgUrl, (newValue) => {
        emit('update:modelValue', newValue);
    });

    const showLoading = () => {
        eventBus.emit('show-loading', 'Uploading image...');
    };

    const onUpload = (event) => {
        const response = JSON.parse(event.xhr.response);
        imgUrl.value = response.url; // This will trigger the watcher and emit the update
        eventBus.emit('hide-loading');
    };

    const handleClearImage = () => {
        imgUrl.value = ''; // This will also trigger the watcher and emit the update
    };
</script>


<style scoped>
    .image-container {
        position: relative;
        display: block; 
    }

    .delete-icon {
        position: absolute;
        top: 0;
        left: 0;
        background-color: red;
        color: white;
        border: none; 
        cursor: pointer; 
    }
</style>

