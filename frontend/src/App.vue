<template>
    <div class="website-container">
        <!-- Header -->
        <header class="header">
            <h1 class="logo">HobbyHub</h1>
            <nav class="nav">
                <router-link class="nav-link" :to="{ name: 'Main Page' }">Main Page</router-link>
                <router-link class="nav-link" :to="{ name: 'Other Page' }">Other Page</router-link>
            </nav>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <RouterView />
        </main>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});
</script>

<style scoped>
/* Global Styles */
body {
    margin: 0;
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f9;
}

.website-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.header {
    background-color: #007bff;
    color: white;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

.nav {
    display: flex;
    gap: 1rem;
}

.nav-link {
    text-decoration: none;
    color: white;
    font-weight: bold;
    transition: color 0.3s ease, background-color 0.3s ease;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}

.nav-link:hover {
    background-color: white;
    color: #007bff;
}




</style>
