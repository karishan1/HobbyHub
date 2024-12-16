<template>
    <div class="h3">
      <ul>
        <li  v-for="user in user_arr" :key="user.id" >
          <p>{{ user.username }}</p>
          <ul>
            <li v-for="hobby in user.hobbies" :key="hobby">
              <p>{{ hobby}}</p>
            </li>
          </ul>

        </li>
      </ul>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";

      interface User {
        id: number,
        username: string,
        hobbies: string[]
      }
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
                  user_arr: [] as User[]
              }
          },
          methods:{
            async fetch_users(){
                const response = await fetch('http://127.0.0.1:8000/user_list/');
                const data = await response.json();
                this.user_arr = data;

            }
          },
          created(){
            this.fetch_users();
          }
      })
  </script>
  
  <style scoped>
  </style>
  