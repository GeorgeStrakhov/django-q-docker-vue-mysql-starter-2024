<template>
    <div v-if="isLoading" class="loading-overlay">
        <div>
            <Loading />
            <div class="text-white text-center">{{ loadingMessage }}</div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { eventBus } from '@/helpers/eventBus';
import { useLoadingStore } from '@/stores/loadingStore';
import { storeToRefs } from 'pinia';

const loadingStore = useLoadingStore();

onMounted(() => {
  eventBus.on('show-loading', loadingStore.showLoading);
  eventBus.on('hide-loading', loadingStore.hideLoading);
});

onUnmounted(() => {
  eventBus.off('show-loading', loadingStore.showLoading);
  eventBus.off('hide-loading', loadingStore.hideLoading);
});

const { isLoading, loadingMessage } = storeToRefs(loadingStore);

</script>

<style>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
</style>

