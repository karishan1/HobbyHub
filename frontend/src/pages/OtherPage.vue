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
                  user_arr: [] as User[],
                  local_user: {
                    id: 100,
                    username: "Sajith",
                    hobbies: ["gaming","golf","football","guitar"]
                  }
              }
          },
          methods:{
            async fetch_users(){
                const response = await fetch('http://127.0.0.1:8000/user_list/');
                const data = await response.json();
                this.user_arr = this.mostCommonHobbies(data, this.local_user);
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
            }


          },
          created(){
            this.fetch_users();
          }
      })
  </script>
  
  <style scoped>
  </style>
  