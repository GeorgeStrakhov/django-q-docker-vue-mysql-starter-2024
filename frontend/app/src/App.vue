<template>
    <Toaster />
    <div class="container">
        <Header />
        <router-view :key="$route.fullPath"></router-view>
        <Footer />
    </div>
</template>

<script>

    import Footer from './components/Footer.vue'
    import Header from './components/Header.vue'
    import Toaster from './components/Toaster.vue'

    export default {
        components:{
            Footer,
            Header,
            Toaster
        }
    }

</script>

<style>
    body {
        font-family: var(--font-family);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
</style>
