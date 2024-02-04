<template>
    <Toast :breakpoints="{'920px': {width: '100%', right: '0', left: '0'}}"/>
</template>

<script setup>
    import { onMounted, onBeforeUnmount } from 'vue';
    import emitter from '@/helpers/eventBus';
    import { useToast } from 'primevue/usetoast';

    const toast = useToast();

    const eventHandler = (payload) => {
        console.log(payload);
        toast.add({severity: payload.severity, summary: payload.summary, detail: payload.detail, life: payload.life});
    };

    onMounted(() => {
      emitter.on('toast', eventHandler);
    });

    onBeforeUnmount(() => {
      emitter.off('toast', eventHandler);
    });

</script>
