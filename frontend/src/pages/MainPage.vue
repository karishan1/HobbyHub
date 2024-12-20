<template>
  <div class="h1">
    <h2>{{ title }}</h2>
    <div v-if="user_profile">
      <p>{{user_profile.username}}</p>
      <p>{{user_profile.password}}</p>
      <p>{{user_profile.email}}</p>
      <p>{{user_profile.DOB}}</p>
      <p>{{user_profile.hobbies}}</p>
    </div>
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";

    interface User {
        id: number,
        username: string,
        password: string,
        email: string,
        DOB: Date,
        hobbies: string[]
      }


    export default defineComponent({
      name: "MainPage",
        data() {
            return {
                title: "Main Page",
                user_id: sessionStorage.getItem('user_id'),
                user_profile : null as User | null,
            }
        },
        methods:{
          async fetch_users(){
                const response = await fetch('http://127.0.0.1:8000/user/');
                const data = await response.json();

                const user = data.find((u: User) => u.id === parseInt(this.user_id!));

                this.user_profile = user;
            }
        },
        created(){
          this.fetch_users();
        }
    })
</script>

<style scoped>
</style>
