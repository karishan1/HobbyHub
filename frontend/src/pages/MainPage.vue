<template>
  <div class="mainpage-container">
    <div class="logout-container">
      <!-- Logout Button-->
      <button @click="logout" class="logout-btn">Logout</button>
    </div>
    <h1 class="title">{{ title }}</h1>

    <div v-if="error" class="error">
      <p>Error: {{ error }}</p>
    </div>

    <div v-else-if="user.username" class="content-container">
      <!-- User Information Blob -->
      <div class="blob user-info">
        <h2>User Information</h2>
        <!-- Editable Form -->
        <div v-if="isEditing">
          <!-- Toggle Between Details and Password Form -->
          <div v-if="isChangingPassword">
            <label class="label">Old Password:</label>
            <input type="password" v-model="passwordForm.oldPassword" class="input" />

            <p v-if="formErrors.old_password" class="form-error">{{ formErrors.old_password[0] }}</p>

            <label class="label">New Password:</label>
            <input type="password" v-model="passwordForm.newPassword" class="input" />

            <label class="label">Confirm New Password:</label>
            <input type="password" v-model="passwordForm.confirmPassword" class="input" />

            <p v-if="formErrors.new_password2" class="form-error">{{ formErrors.new_password2[0] }}</p>

            <button @click="changePassword" class="save-btn">Change Password</button>
            <button @click="cancelPasswordChange" class="cancel-btn">Cancel</button>
          </div>

          <div v-else>
            <label class="label">Username:</label>
            <input type="text" v-model="editedUser.username" class="input" />
            <p v-if="formErrors.username" class="form-error">{{ formErrors.username[0] }}</p>

            <label class="label">Email:</label>
            <input type="email" v-model="editedUser.email" class="input" />
            <p v-if="formErrors.email" class="form-error">{{ formErrors.email[0] }}</p>

            <label class="label">DOB:</label>
            <input type="date" v-model="editedUser.DOB" class="input" />
            <p v-if="formErrors.DOB" class="form-error">{{ formErrors.DOB[0] }}</p>

            <p v-if="formError" class="form-error">{{ formError }}</p>

            <button @click="saveDetails" class="save-btn">Save</button>
            <button @click="cancelEdit" class="cancel-btn">Cancel</button>
            <button @click="togglePasswordChange" class="edit-btn-1">Change Password</button>
          </div>

        </div>

        <!-- Display User Info -->
        <div v-else>
          <p><span class="label">Username:</span> {{ user.username }}</p>
          <p><span class="label">Email:</span> {{ user.email }}</p>
          <p><span class="label">DOB:</span> {{ user.DOB }} </p>
          <button @click="editDetails" class="edit-btn">Edit Details</button>
          <button @click="showRequestsModal = true" class="show-requests">Show Friend Requests</button>
        </div>
      </div>

      <!-- Hobbies Blob -->
      <div class="blob hobbies">
        <h2>Hobbies</h2>
        <ul class="hobby-list">
          <li v-for="hobby in user.hobbies" :key="hobby">
            <p>{{ hobby }}</p>
            <button @click="removeHobby(hobby)">X</button>
          </li>
        </ul>
        <button @click="showHobbiesModal = true" class="edit-btn">Edit Hobbies</button>
      </div>
    </div>
    
      <div v-if="showHobbiesModal" class="modal">
        <div class="modal-content">
          <h4>Add hobby</h4>
          <div class="add_new_hobby">
            <input v-model="newHobbyName" placeholder="Enter your own hobby" />
            <button @click="addNewHobby" class="add-btn">Add Hobby</button>
          </div>
          <h4 style="margin-top: 1.3rem;">Choose from available hobbies</h4>
          <ul class="choose_hobby">
            <li  v-for="hobby in availableHobbies.filter(h => !userStore.hobbies.includes(h.hobby_name))" :key="hobby.id" >
              <p>{{ hobby.hobby_name }}</p>
              <button @click="addExistingHobby(hobby.id)" class="add-btn">Add</button>
            </li>
          </ul>
          <button style="align-self: flex-end; margin-right: 0.8rem;" @click="showHobbiesModal = false" class="cancel-btn">Close</button>
        </div>
      </div>
      <div v-if="showRequestsModal == true" class="modal">
        <div class="modal-content-requests">
          <h4 style="margin-top: 1rem;">Pending Freind Requests</h4>
          <div class="modal-request-container">
            <ul v-if="friendRequests.length > 0">
              <li v-for="x in friendRequests" :key="x.id" >
                <div v-if="x.status == 'pending'">
                  <p>Friend request from  {{ x.from_user_username }}</p>
                  <button class="accept" @click="acceptRequest(x.id)">Accept</button>
                </div>
              </li>
            </ul>
            <div v-else  class="no-requests"> No Friend Requests</div>
          </div>
          <button @click="showRequestsModal = false" class="close-request-modal">Close</button>
        </div>
      </div>

  </div>
</template>

<script lang="ts">
import { useUserStore } from '../stores/userStore';
import { defineComponent } from "vue";

interface Hobby {
  id: number;
  hobby_name: string;
}

interface User {
  username: string;
  email: string;
  DOB: string;
  hobbies: string[];
}
interface FriendRequest {
  id : number,
  from_user_id : number,
  from_user_username : string,
  status : string
}

export default defineComponent({
  name: "MainPage",

  data() {
    return {
      title: "User Dashboard",
      user: {} as User,
      editedUser: {} as User,
      availableHobbies: [] as Hobby[],
      friendRequests: [] as FriendRequest[],
      newHobbyName: "",
      passwordForm: {
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      },
      isEditing: false,
      isChangingPassword: false,
      error: null as string | null,
      formError: null as string | null,
      showHobbiesModal: false,
      showRequestsModal: false,
      formErrors: {} as { [key: string]: string[] },
      csrfToken: "",
    };
  },
  computed: {
        userStore(){
            return useUserStore();
        }
    },
  methods: {
    async fetch_csrf_token(){
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
    async fetchUser() { 
       // Fetches current user data
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
    async fetchRequests(){
      fetch("http://127.0.0.1:8000/send_friend_request/", {
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
        this.friendRequests = data;

      })
      .catch((error) => {
        this.error = error.message;
      });

    },
    async acceptRequest(id:number){
      const url = "http://127.0.0.1:8000/send_friend_request/";

      try{
        const response = await fetch(url,{
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          credentials: "include",
          body: JSON.stringify({request_id: id}),
        });

        if (response.ok){
          this.fetchRequests();
          alert(`Friend request accepted`);
          
        }
        else{
          const error = await response.json();
          alert(`${error.message}`);

        }
      }
      catch(error) {
        alert(`Error`);
      }
    },

    async fetchHobbies() {
      try {
        const response = await fetch("http://127.0.0.1:8000/display_hobby/", {
          method: "GET",
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch hobbies: ${response.status}`);
        }
        this.availableHobbies = await response.json();
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },

    async addExistingHobby(hobbyId: number) {
      try {
 
        const response = await fetch("http://127.0.0.1:8000/add_user_hobby/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify({ hobby_id: hobbyId }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to add existing hobby: ${response.status}`);
        }

        const hobby = this.availableHobbies.find((h) => h.id === hobbyId);
        if (hobby && !this.user.hobbies.includes(hobby.hobby_name)) {
          this.user.hobbies.push(hobby.hobby_name);
          this.fetchUser();
        }
      } catch (error) {
        console.error("Error adding existing hobby:", error);
      }
    },

    async addNewHobby() {
      if (!this.newHobbyName.trim()) {
        alert("Hobby name cannot be empty.");
        return;
      }
      try {
        const response = await fetch("http://127.0.0.1:8000/add_hobby_to_db/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify({ hobby_name: this.newHobbyName }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to add new hobby to the database: ${response.status}`);
        }

        this.newHobbyName = "";
        await this.fetchHobbies();
      } catch (error) {
        console.error("Error adding new hobby to the database:", error);
      }
    },

    async removeHobby(hobbyName: string) {
      try {

        const response = await fetch("http://127.0.0.1:8000/remove_user_hobby/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,          
          },
          body: JSON.stringify({ hobby_name: hobbyName }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to remove hobby: ${response.status}`);
        }

        this.user.hobbies = this.user.hobbies.filter((hobby) => hobby !== hobbyName);
        this.fetchUser();

      } catch (error) {
        console.error("Error removing hobby:", error);
      }
    },

    editDetails() {
      this.editedUser = { ...this.user };
      this.isEditing = true;
    },

    async saveDetails() {
      this.formErrors = {}; 
      this.formError = null; 

      try {
        const response = await fetch("http://127.0.0.1:8000/api/current-user/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          credentials: "include",
          body: JSON.stringify(this.editedUser),
        });

        if (!response.ok) {
          const errorData = await response.json();

          if (errorData.errors) {
            this.formErrors = errorData.errors;
          } else {
            this.formError = "An unexpected error occurred while updating details.";
          }
          return;
        }

        this.isEditing = false;
        this.fetchUser();
        alert("User details updated successfully!");
      } catch (error) {
        this.formError = error instanceof Error ? error.message : String(error);
      }
    },

    logout() {
      fetch('/logout/', {
        method: 'GET',
        credentials: 'include',
      }).then(() => {
        window.location.href = 'http://127.0.0.1:8000/'; // Redirect to the login page
      }).catch(error => {
        console.error('Error logging out:', error);
      });
    },

    cancelEdit() {
      this.isEditing = false;
      this.isChangingPassword = false;
    },

    togglePasswordChange() {
      this.isChangingPassword = !this.isChangingPassword;
    },

    cancelPasswordChange() {
      this.isChangingPassword = false;
      this.passwordForm = {
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      };
    },
    
    async changePassword() {
        this.formErrors = {}; // Reset errors

        try {
          const response = await fetch("http://127.0.0.1:8000/change-password/", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.csrfToken,
            },
            credentials: "include",
            body: JSON.stringify({
              old_password: this.passwordForm.oldPassword,
              new_password1: this.passwordForm.newPassword,
              new_password2: this.passwordForm.confirmPassword,
            }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            if (errorData.errors) {
              this.formErrors = errorData.errors; 
            } else {
              alert("An error occurred while changing the password.");
            }
            return;
          }

          alert("Password changed successfully!");
          this.cancelPasswordChange();
        } catch (error) {
          console.error("Error:", error);
          alert("An error occurred. Please try again.");
        }
      }



    },

  async mounted() {
    await this.fetch_csrf_token();
    this.fetchUser();
    this.fetchHobbies();
    this.fetchRequests();
  },
});
</script>


  <style scoped>
  /* Main Container */
  .mainpage-container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 1rem;
    font-family: Arial, sans-serif;
    position: relative;
  }

  /* Title */
  .title {
    text-align: center;
    font-size: 2rem;
    color: #333;
    margin-bottom: 1.5rem;
  }

  /* Error */
  .error {
    color: red;
    text-align: center;
    font-weight: bold;
    background-color: #ffe6e6;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
  }

  /* Content Container */
  .content-container {
    display: flex;
    gap: 2rem;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
  }

  /* Blob Styling */
  .blob {
    background-color: #f9f9f9;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    flex: 1;
    max-width: 45%;
    min-width: 300px;
  }

  /* Labels */
  .label {
    font-weight: bold;
    color: #007bff;
  }

  /* Input */
  .input {
    display: block;
    margin: 0.5rem 0 1rem;
    padding: 0.5rem;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  /* Buttons */
  .edit-btn,
  .save-btn,
  .cancel-btn {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 1rem;
  }
  .edit-btn-1{
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 1rem;
    margin-left: 8rem;

  }

  .save-btn {
    background-color: #28a745;
  }

  .cancel-btn {
    background-color: #dc3545;
    margin-left: 1rem;
  }

  .edit-btn:hover,
  .save-btn:hover,
  .cancel-btn:hover {
    opacity: 0.8;
  }

  /* Hobbies List */
  .hobby-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 12rem;
    overflow-y: auto;
  }

  .hobby-list li{
    display: flex;
    flex-direction: row;
    width: auto;
    background-color: white;
    align-items: center;
    color: black;
    height: 2.5rem;
    border-radius: 0.3rem;
    padding-left: 1rem;
    gap: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
    border: 1.5px black solid;
    border-right: none;
  }

  .hobby-list li p{
    margin: 0;
    padding: 0;
  }

  .hobby-list button{
    height: 2.5rem;
    border: none;
    width: auto;
    background-color: #dc3545;
    border-top-right-radius: 0.3rem;
    border-bottom-right-radius: 0.3rem;
    color: white;
    padding-left: 0.9rem;
    padding-right: 0.9rem;
  }

  .hobby-list button:hover{
    background-color: #ff5162;

  }



  /* Loading */
  .loading {
    text-align: center;
    font-size: 1.2rem;
    color: #555;
  }

  .form-error {
    color: red;
    font-size: 0.9rem;
    margin-top: 0.3rem;
  }

  .modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

.modal-content h4{
  align-self: flex-start;
  margin-left: 1rem;
}

.choose_hobby{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 27rem;
  max-height: 15rem;
  margin: 0;
  padding: 0;
  gap: 0.5rem;
  overflow-y: auto;
}
.choose_hobby li {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  width: auto;
  background-color: white;
  color: black;
  height: 2.5rem;
  border-radius: 0.3rem;
  padding-left: 1rem;
  gap: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
  border: 1.5px black solid;
  border-right: none;
}
.choose_hobby li p{
  margin: 0;
  padding: 0;
}

.choose_hobby li button{
  border: none;
  font-size: 0.85rem;
  height: 2.5rem;
  background-color: #0aa32e;
  border-top-right-radius: 0.3rem;
  border-bottom-right-radius: 0.3rem;
  padding-left: 0.7rem;
  padding-right: 0.7rem;
  color: white;
  border: 1.5px #0aa32e solid;

}

.choose_hobby li button:hover{
  background-color: #1bce44;
  border: 1.5px #1bce44 solid;
}

.add_new_hobby{
  margin-top: 0.5rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 27rem;
}

.add_new_hobby input{
  width: 18rem;
  height: 2.4rem;
  border-radius: 0.3rem;
  border: black 1.5px solid;
  font-size: 1rem;
  padding-left: 0.5rem;
}

.add_new_hobby button{
  color: white;
  background-color: #0aa32e;
  font-size: 0.9rem;
  border: none;
  width: 8rem;
  border-radius: 0.3rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
}

.add_new_hobby button:hover{
  background-color: #0aa32ec8;
  transition: 0.2s ease;
}



.remove-btn {
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  margin-left: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  background: #c82333;
}

.scrollable-list {
  max-height: 200px; /* Set a maximum height for the list */
  overflow-y: auto;  /* Enable vertical scrolling */
  border: 1px solid #ccc; /* Optional: Add a border for better visibility */
  padding: 0.5rem; /* Optional: Add some padding */
  border-radius: 5px; /* Optional: Add rounded corners */
}
.friend-request-container{
  justify-self: flex-end;
  background-color: #007bff;
  width: 33rem;
  height: 20rem;
}

.modal-content-requests{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  border-radius: 1rem;
  width: 40rem;
  height: 30rem;
  gap: 1rem;
}
.modal-request-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 21rem;
  width: 35rem;

}

.modal-request-container ul{
  list-style: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: auto;

  max-height: 22rem;
  overflow-y: auto;
}
.modal-request-container li div{
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 35rem;
  height: 3.5rem;
  margin-right: 2rem;
  gap: 2rem;
  margin-top: 1rem;
}
.modal-request-container li div p{
  display: flex;
  align-items: center;
  margin-top: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
  border-radius: 0.5rem;
  height: 3rem;
  padding-right: 1rem;
  padding-left: 1rem;
  background-color: #007bff;
  color: white;
}
.accept{
  border: none;
  height: 3rem;
  width: 6rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
  background-color: #0aa32e;
  color: white;
  font-size: 1rem;
}
.accept:hover{
  background-color: #05c732;
  transition: ease 0.3s;
}
.close-request-modal{
  background-color: #c82333;
  color: white;
  align-self: flex-end;
  margin-right: 2rem;
  border: none;
  width: 5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
}
.close-request-modal:hover{
  background-color: #f02b3e;
  transition: ease 0.1s;

}
.no-requests{
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 7rem;
  background-color: #b5b5b5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.248);
  width: 20rem;
  height: 6rem;
  color: white;
  font-size: 1.4rem;
  border-radius: 0.7rem;
}
.show-requests{
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 1rem;
  margin-left: 9rem;
}
.logout-btn {
  background-color: #dc3545; 
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}
.logout-btn:hover {
  opacity: 0.8;
}
.logout-container {
  position: absolute; 
  top: 10px; 
  right: -80px; 
}

.form-error {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

</style>