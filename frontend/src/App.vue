<template>
    <div class="website-container">
        <!-- Header -->
        <header class="header">
            <h1 class="logo">My Website</h1>
            <nav class="nav">
                <router-link class="nav-link" :to="{ name: 'Main Page' }">Main Page</router-link>
                <router-link class="nav-link" :to="{ name: 'Other Page' }">Other Page</router-link>
            </nav>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <RouterView />
        </main>

        <!-- Footer -->
        <footer class="footer">
            <p>&copy; 2025 HobbyHub</p>
        </footer>
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

/* Website Container */
.website-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Header */
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

/* Main Content */
.main-content {
    flex: 1;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Footer */
.footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    font-size: 0.9rem;
    margin-top: auto;
}

.footer p {
    margin: 0;
}
</style>
