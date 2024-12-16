<template>
    <div class="h3">
      {{ user_arr }}
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
                  user_arr: []
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
  