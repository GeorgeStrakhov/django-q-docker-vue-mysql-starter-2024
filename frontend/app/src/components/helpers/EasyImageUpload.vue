<template>
    <div>
        <div v-if="imgUrl">
            <div class="image-container">
                <img :src="imgUrl" alt="Uploaded image" width="200" />
                <button class="delete-icon" @click="handleClearImage">X</button>
            </div>
        </div>
        <div v-else>
            <FileUpload mode="basic" name="img_upload" url="/api/img_upload/" @beforeUpload="showLoading" @upload="onUpload" accept="image/*" :fileLimit="1" :maxFileSize="maxFileSize" :auto="true" />
        </div>
    </div>
</template>

<script>
import FileUpload from 'primevue/fileupload';
import { eventBus } from '@/helpers/eventBus';

export default {
    components: {
        FileUpload,
    },
    props: {
        initialImgUrl: {
            type: String,
            default: '',
        },
        maxFileSize: {
            type: Number,
            default: 2000000, // 2MB default max file size
        },
    },
    data() {
        return {
            imgUrl: this.initialImgUrl,
        };
    },
    methods: {
        showLoading() {
            eventBus.emit('show-loading', 'Uploading image...');
        },
        onUpload(event) {
            const response = JSON.parse(event.xhr.response);
            this.imgUrl = response.url;
            this.$emit('update:imgUrl', this.imgUrl); // Emit an event to update the parent component
            eventBus.emit('hide-loading');
        },
        handleClearImage() {
            this.imgUrl = '';
            this.$emit('update:imgUrl', this.imgUrl); // Clear the image and notify the parent component
        },
    },
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

