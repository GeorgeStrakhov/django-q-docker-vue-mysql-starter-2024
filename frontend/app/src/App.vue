<template>
    <Toast :breakpoints="{'920px': {width: '100%', right: '0', left: '0'}}"/>
    <div class="container">
        <Header />
        <router-view :key="$route.fullPath"></router-view>
        <Footer />
    </div>
</template>

<script>

    import Footer from './components/Footer.vue'
    import Header from './components/Header.vue'

    export default {
        components:{
            Footer,
            Header
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
