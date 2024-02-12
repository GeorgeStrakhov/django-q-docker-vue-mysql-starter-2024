<script setup>

import { ref, onMounted } from 'vue';
const showDialog = ref(false);

onMounted(() => {
  if (!localStorage.getItem('cookieConsent')) {
    showDialog.value = true;
  }
});

const handleOk = () => {
  localStorage.setItem('cookieConsent', 'true');
  showDialog.value = false;
};
</script>

<template>
    <Dialog modal :visible.sync="showDialog" position="bottomleft" :draggable="false" :closable="false">
        <h1>🍪 🍪 🍪</h1>
        We use 'em tasty cookies to make this thing work. Hope you don't mind ;)
        <template #footer>
            <Button label="Ok" @click="handleOk" />
        </template>
    </Dialog>
</template>
