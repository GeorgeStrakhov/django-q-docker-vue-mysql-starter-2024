<template>
  <div class="flex w-full relative align-items-center justify-content-start my-3 px-4">
    <div class="border-top-1 surface-border top-50 left-0 absolute w-full">
        <p class="text-center text-color-secondary">{{projectName}} | &copy; {{(new Date()).getFullYear()}} | {{contactEmail}}</p>
    </div>
  </div>
</template>

<script setup>
    const projectName = import.meta.env.VITE_PROJECT_NAME;
    const contactEmail = import.meta.env.VITE_CONTACT_EMAIL;
</script>
