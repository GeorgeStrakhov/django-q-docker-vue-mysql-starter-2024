<template>
    <Toaster />
    <GlobalLoading />
    <ConfirmPopup></ConfirmPopup>
    <div class="container">
        <Header />
        <div class="p-4 lg:p-6">
            <router-view :key="$route.fullPath"></router-view>
        </div>
        <Footer />
    </div>

    <CookieConsent />

</template>

<script>
    import Footer from './components/Footer.vue'
    import Header from './components/Header.vue'
    import CookieConsent from './components/CookieConsent.vue'
    import Toaster from './components/Toaster.vue'
    import GlobalLoading from './components/GlobalLoading.vue'

    export default {
        components:{
            Footer,
            Header,
            Toaster,
            GlobalLoading,
            CookieConsent
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
