<template>
    <div class="list-container">
      <ul>
        <li class="user-container"  v-for="user in user_arr"   :key="user.id" >
            <div class="div-1">
              <p>Name:</p>
              <p class="name">{{ user.username }}</p>
              <button class="add_button">Add Friend</button>
            </div>
            <div class="div-2">
              <p>Hobbies:</p>
              <ul class="hobby-container">
                <li class="hobby-box"  v-for="hobby in user.hobbies" :key="hobby" >{{ hobby}}</li>
              </ul>
            </div>
        </li>
      </ul>
    </div>
  
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
      import { useUserStore } from '../stores/userStore';
      

      interface User {
        id: string,
        username: string,
        hobbies: string[]
      }
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
                  user_arr: [] as User[],
              }
          },
          setup(){
            const userStore = useUserStore();
            userStore.loadUser();

            return {userStore};
          },
          computed: {
              local_user():User{
                return{
                  id: this.userStore.user_id,
                  username: this.userStore.username,
                  hobbies: this.userStore.hobbies
                };
              },
          },
          methods:{
            async fetch_users(){
              fetch("http://127.0.0.1:8000/user_list/", {
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
                    this.user_arr = data; 

                  })
                  .catch((error) => {
                    error = error.message; 
                  });
            },
            mostCommonHobbies(user_arr: User[], local_user: User): User[]{
              function getCommonHobbyCount(user_hobbies : string[], local_user_hobbies : string[]): number{
                let commonHobbyCount: number = 0;

                for (let x of user_hobbies){
                  for (let y of local_user_hobbies){
                    if (x === y){
                      commonHobbyCount += 1;
                      break;
                    }
                  }
                }
                return commonHobbyCount;
              }

              for (let i = 0; i < user_arr.length; i++){
                for (let j = i+1; j < user_arr.length; j++){
                  const commonHobbyCountA = getCommonHobbyCount(user_arr[i].hobbies,local_user.hobbies);
                  const commonHobbyCountB = getCommonHobbyCount(user_arr[j].hobbies,local_user.hobbies);

                  if (commonHobbyCountB > commonHobbyCountA){
                    const cur = user_arr[i];
                    user_arr[i] = user_arr[j];
                    user_arr[j] = cur;
                  }
                }
              }

              return user_arr
            },


          },
          mounted(){
            this.fetch_users();
          }
      })
  </script>
  
  <style scoped>

  .list-container{
    display: flex;
    align-items: center;
    justify-content: flex-start;
    width: 100vw;
    height: 100vh;
    margin-top: 10rem; 
  }
  ul{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    list-style-type: none;
  }

  .user-container{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 1rem;
    background-color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    border-radius: 1rem;
    width: 40rem;

  }

  .hobby-container{
    display: flex;
    flex-direction: row;
    gap: 1rem;
    padding: 1rem;
    background-color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    border-radius: 0.5rem;
    max-width: 33rem;
    margin-left: 1rem;
  }
  .hobby-box{
    color: white;
    padding: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.3rem;
    align-self: center;
    background-color: #057BFF;
  }

  .name{
    color: white;
    background-color: #007BFF;
    padding: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    border-radius: 0.3rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    margin-left: 1rem;
  }

  .div-1{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    max-width: 38rem;
  }
  .div-2{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    justify-items: center;
  }      
  </style>
  