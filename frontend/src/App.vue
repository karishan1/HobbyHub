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
  
      <!-- Footer -->
      <footer class="footer">
        <p>&copy; 2025 HobbyHub. All rights reserved.</p>
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
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
  }
  
  body {
    background-color: #f4f4f9;
    color: #333;
    height: 100%;  /* Ensure the body fills the page height */
  }
  
  /* This container ensures the entire layout (header, content, footer) is arranged in a column */
  .website-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    height: 100%;
  }
  
  .main-content {
    flex-grow: 1; /* Ensures content takes available space */
    overflow-y: auto; /* Allows content to scroll if necessary */
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
    font-weight: 600;
    margin: 0;
  }
  
  .nav {
    display: flex;
    gap: 1rem;
  }
  
  .nav-link {
    text-decoration: none;
    color: white;
    font-weight: 600;
    transition: color 0.3s ease, background-color 0.3s ease;
    padding: 0.5rem 1rem;
    border-radius: 5px;
  }
  
  .nav-link:hover {
    background-color: white;
    color: #007bff;
  }
  
  .footer {
    background-color: #333;
    color: white;
    padding: 1rem;
    text-align: center;
    font-size: 0.9rem;
    margin-top: auto; /* Ensures footer stays at the bottom */
  }
  </style>
  