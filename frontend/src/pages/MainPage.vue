<template>
  <div>
    <h1>{{ title }}</h1>
    <div v-if="error">
      <p>Error: {{ error }}</p>
    </div>
    <div v-else-if="user.username">
      <p>Username: {{ user.username }}</p>
      <p>Email: {{ user.email }}</p>
      <p>DOB: {{ userStore.DOB }}</p>
      <ul>
        <li v-for="hobby in user.hobbies" :key="hobby">{{ hobby }}</li>
      </ul>
    </div>
    <div v-else>
      <p>Loading user data...</p>
    </div>
  </div>
</template>

<script>

import { useUserStore } from '../stores/userStore';
export default {
  name: "MainPage",
  data() {
    return {
      title: "Main Page",
      user: {
        username: "",
        email: "",
        DOB: "",
        hobbies: [],
      },
      error: null,
    };
  },
  computed: {
        userStore(){
            return useUserStore();
        }
    },
  methods: {
    fetchUser() {
      fetch("http://127.0.0.1:8000/api/current-user/", {
        method: "GET",
        credentials: "include", 
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          this.user = data; 
          this.userStore.setUser(data.id, data.username, data.hobbies);
        })
        .catch((error) => {
          this.error = error.message; 
        });
    },
  },
  created() {
    this.fetchUser(); 
  },
};
</script>

<style scoped>
</style>
