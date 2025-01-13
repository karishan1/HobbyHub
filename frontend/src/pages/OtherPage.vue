<template>
  <div class="list-container">
    <div class="filter-container">
      <div class="filter-input-container">
        <div class="filter-input">
          <label>Min age:</label>
          <input type="number" id="min_age" v-model.number="minAge" min="0"/>
        </div>
        <div class="filter-input">
          <label>Max age:</label>
          <input type="number" id="max_age" v-model.number="maxAge" min="0"/>
        </div>
      </div>
      <button @click="filterByAge" class="filter_button">Filter</button>
    </div>
    <div v-if="loading">
      <p>Loading ...</p>
    </div>
    <div v-else>
      <ul>
        <li class="user-container"  v-for="user in user_arr"   :key="user.id ?? 0" >
            <div class="div-1">
              <div class="div-11">
                <p>Name:</p>
                <p class="name">{{ user.username }}</p>
              </div>
              <button v-if="!friend_list.includes(user.id ?? 0)" class="add_button" @click="sendFriendRequest(user.id ?? 0)">Add Friend</button>
              <button v-else class="add_button" disabled style="background-color: #007BFF;">Friend</button>
            </div>
            <div class="div-2">
              <p>Hobbies:</p>
              <ul class="hobby-container">
                <li class="hobby-box" v-if="user.hobbies.length > 0"  v-for="hobby in user.hobbies" :key="hobby" >{{ hobby}}</li>
                <li v-else class="hobby-box" style="background-color: #d80606;">No hobbies </li>
              </ul>
            </div>
        </li>
        <div class="paginator-container" v-if="user_arr.length > 0">
          <button class="page-button" :disabled="!hasPrevious" @click="fetch_users(currentPage -1)">Previous</button>
          <button class="page-button" :disabled="!hasNext" @click="fetch_users(currentPage + 1)">Next</button>
        </div>
        <div v-else-if="user_arr.length == 0" class="no-users">
          <p>No users in the age range</p>
        </div>
      </ul>
    </div>

  </div>

</template>

<script lang="ts">


import { defineComponent } from "vue";
import { useUserStore } from '../stores/userStore';


interface User {
  readonly id: number | null,
  readonly username: string | null,
  readonly hobbies: string[]
}

interface Friend {
  readonly friend_id: number,
  readonly friend_name: string,
}

export default defineComponent({
    data() {
        return {
            title: "Other Page" as string,
            user_arr: [] as User[],
            friend_list: [] as  number[],
            minAge: 0 as number,
            maxAge: 100 as number,
            csrfToken: "" as string,
            currentPage: 1 as number,
            totalPages: 1 as number,
            hasNext: false as boolean,
            hasPrevious: false as boolean,
            loading: true as boolean,
        }
    },
    setup(){
      const userStore = useUserStore();
      userStore.loadUser();
      return {userStore};
    },
    computed: {
      local_user(): User{
        return{
          id: this.userStore.user_id || null,
          username: this.userStore.username || null,
          hobbies: this.userStore.hobbies || null,
        };
      },
    },
    methods:{
      async fetch_csrf_token(): Promise<void> {
        const url = new URL("http://127.0.0.1:8000/get_csrf_token/");
        try{
          const response = await fetch(url,{
            method: "GET",
            credentials: "include", 
          });

          if (response.ok){
            const data = await response.json();
            this.csrfToken = data.csrfToken;
            console.log(`Fetched csrf token: ${this.csrfToken}`);
          }
          else{
            console.log(`Failed to fetch token, ${response.statusText}`)
          }
        }
        catch (error){
          console.error(`Error fetching token, ${error}`)
        }
      },
      async fetch_friends(): Promise<void> {
        fetch("http://127.0.0.1:8000/friendships/", {
          method: "GET",
          credentials: "include",
        })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data: Friend[]) => {
          this.friend_list = data.map((friend) => friend.friend_id);
        })
        .catch((error) => {
          alert(error.message);
        });
      },
      async fetch_users(page = 1): Promise<void> {

        this.loading = true;

        const url = new URL("http://127.0.0.1:8000/user_list/");

        url.searchParams.append("page", page.toString());
        if (this.minAge) url.searchParams.append("min_age", this.minAge.toString());
        if (this.maxAge) url.searchParams.append("max_age", this.maxAge.toString());

        fetch(url.toString(), {
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
            this.user_arr = data.user_list; 
            this.currentPage = data.current_page;
            this.totalPages = data.total_pages;
            this.hasNext = data.has_next;
            this.hasPrevious = data.has_previous;

            this.loading = false;
          })
          .catch((error) => {
            error = error.message; 
          });
      },

      filterByAge(): void {
        this.fetch_users();
      },
      async sendFriendRequest(friend_id : number): Promise<void> {
        const url = "http://127.0.0.1:8000/friend_request/";

        try{
          const response = await fetch(url,{
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.csrfToken,
            },
            credentials: "include",
            body: JSON.stringify({to_friend_id: friend_id}),
          });

          if (response.ok){
            alert(`Friend request sent to ${friend_id}`);
          }
          else{
            const error = await response.json();
            alert(`${error.message}`);

          }
        }
        catch(error) {
          alert(`Error`);
        }
      }
    },
    async mounted(){
      await this.fetch_csrf_token();
      this.fetch_friends();
      this.fetch_users();
    }
})
</script>

<style scoped>

.no-users{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #a1a1a1;
  color: white;
  width: 40rem;
  height: 10rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  font-size: 2rem;
  border-radius: 1rem;
}

.paginator-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin-top: 1rem;
  margin-bottom: 3rem;

}
.page-button{
  border: none;
  width: 10rem;
  height: 2rem;
  background-color: #007BFF;
  color: white;
  border-radius: 0.3rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.page-button:hover{
  background-color: #007bffa1;
  transition: 0.3s ease;

}

.page-button:disabled{
  background-color: white;
  color: black;
}

.list-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100vw;
  height: 100vh;
  margin-top: 1rem; 
  gap: 2rem;
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

.filter-container{
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: 4rem;
}
.filter-input-container{
  display: flex;
  flex-direction: row;
  gap: 2rem;
  margin-left: 2rem;
}

.filter-input{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  height: 3rem;
  width: 10rem;
  background-color: #6f6f70;
  gap: 1rem;
  border-radius: 0.7rem;
  color: white;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.filter-input input{
  display: flex;
  flex-direction: row;
  height: 2rem;
  width: 3rem;
  border-radius: 0.7rem;
  border: none;
}

.filter_button{
  background-color: #007BFF;
  color: white;
  border: none;
  width: 8rem; 
  border-radius: 0.7rem; 
  margin-left: 5.5rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.filter_button:hover{
  background-color: #479ffd;
  transition: 0.3s ease;
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
  background-color: #5009d3;
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
  align-items: flex-start;
  justify-content: space-between;
  width: 38rem;
  max-width: 38rem;
}
.div-11{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
}
.div-2{
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  justify-items: center;
}    
.add_button{
  background-color: #06804d;
  color: white;
  padding: 0.5rem;
  padding-left: 1rem;
  padding-right: 1rem;
  font-size: 0.9rem;
  border: none;
  border-radius: 0.3rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  width: 8rem;
}  

.add_button:hover{
  background-color: #069f5f;
  transition: 0.3s ease;
}
</style>