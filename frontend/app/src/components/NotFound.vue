<template>

    <div class="text-center mb-5">
        <Card>
        <template #content>
            <h1>404</h1>
            <h3>sorry, nothing around here</h3>
        </template>
        <template #footer>
            <div class="text-center">
                <router-link to="/">
                    <Button label="go home" />
                </router-link>
            </div>
        </template>
        </Card>
    </div>

</template>
