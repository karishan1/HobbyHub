<template>
  <div class="mainpage-container">
    <h1 class="title">{{ title }}</h1>

    <div v-if="error" class="error">
      <p>Error: {{ error }}</p>
    </div>

    <div v-else-if="user.username" class="content-container">
      <!-- User Information Blob -->
      <div class="blob user-info">
        <div style="display: flex; flex-direction: row; justify-content: space-between; margin-bottom: 1rem;">
          <h2>User Information</h2>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
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
            <h4>Add Hobby</h4>
            <div class="add_new_hobby">
                <input v-model="newHobbyName" placeholder="Enter your own hobby" class="input-field"/>
                <button @click="addNewHobby" class="add-btn">Add Hobby</button>
            </div>
            <h4 style="margin-top: 1.3rem;">Choose from available hobbies</h4>
            <ul class="choose_hobby">
                <li v-for="hobby in availableHobbies.filter(h => !userStore.hobbies.includes(h.hobby_name))" :key="hobby.id">
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
interface PasswordForm{

  oldPassword: string
  newPassword: string,
  confirmPassword: string,
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
      newHobbyName: "" as string,
      passwordForm: {} as PasswordForm,
      isEditing: false as boolean,
      isChangingPassword: false as boolean,
      error: null as string | null,
      formError: null as string | null,
      showHobbiesModal: false as boolean,
      showRequestsModal: false as boolean,
      formErrors: {} as { [key: string]: string[] },
      csrfToken: "" as string,
    };
  },
  computed: {
        userStore(): ReturnType<typeof useUserStore>{
            return useUserStore();
        }
    },
  methods: {
    getBaseURL(): string {
      const hostname = window.location.hostname;
      
      if (hostname === "localhost" || hostname === "127.0.0.1") {
        return "http://127.0.0.1:8000/"; 
      }

      return "https://group4-web-apps-ec22899.apps.a.comp-teach.qmul.ac.uk/";
    },
    async fetch_csrf_token(): Promise<void>{
      const url = new URL(`${this.getBaseURL()}get_csrf_token/`);
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
    async fetchUser(): Promise<void> { 
       // Fetches current user data
      fetch(`${this.getBaseURL()}current-user/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.csrfToken,
        },
        credentials: "include",
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        this.user = data as User;
        this.userStore.setUser(data.id, data.username, data.hobbies);
      })
      .catch((error) => {
        this.error = error instanceof Error ? error.message : "Unexpected error";
      });
    },
    async fetchRequests(): Promise<void>{
      fetch(`${this.getBaseURL()}friend_request/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.csrfToken,
        },
        credentials: "include",
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        this.friendRequests = data as FriendRequest[];

      })
      .catch((error) => {
        this.error = error instanceof Error ? error.message : "Unexpected error";
      });

    },
    async acceptRequest(id:number): Promise<void>{
      const url = `${this.getBaseURL()}friend_request/`;

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
    async fetchHobbies(): Promise<void> {
      try {
        const response = await fetch(`${this.getBaseURL()}hobby_db/`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error(`Failed to fetch hobbies: ${response.status}`);
        }
        this.availableHobbies = await response.json();
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },

    async addExistingHobby(hobbyId: number): Promise<void> {
      try {
 
        const response = await fetch(`${this.getBaseURL()}current-user/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify({ hobby_id: hobbyId, action: "add hobby" }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to add existing hobby: ${response.status}`);
        }
        this.fetchUser();

      } catch (error) {
        console.error("Error adding existing hobby:", error);
      }
    },

    async addNewHobby(): Promise<void> {
      if (!this.newHobbyName.trim()) {
        alert("Hobby name cannot be empty.");
        return;
      }
      try {
        const response = await fetch(`${this.getBaseURL()}hobby_db/`, {
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

    async removeHobby(hobbyName: string): Promise<void> {
      try {

        const response = await fetch(`${this.getBaseURL()}current-user/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,          
          },
          body: JSON.stringify({ hobby_name: hobbyName, action: "remove hobby" }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to remove hobby: ${response.status}`);
        }
        this.fetchUser();

      } catch (error) {
        console.error("Error removing hobby:", error);
      }
    },

    editDetails(): void {
      this.editedUser = { ...this.user };
      this.isEditing = true;
    },

    async saveDetails(): Promise<void> {
      this.formErrors = {}; 
      this.formError = null; 

      try {
        const response = await fetch(`${this.getBaseURL()}current-user/`, {
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

    async logout(): Promise<void> {
      fetch('/logout/', {
        method: 'GET',
        credentials: 'include',
      }).then(() => {
        window.location.href = `${this.getBaseURL()}`; 
      }).catch(error => {
        console.error('Error logging out:', error);
      });
    },

    cancelEdit(): void {
      this.isEditing = false;
      this.isChangingPassword = false;
    },

    togglePasswordChange(): void {
      this.isChangingPassword = !this.isChangingPassword;
    },

    cancelPasswordChange(): void {
      this.isChangingPassword = false;
      this.passwordForm = {
        oldPassword: "",
        newPassword: "",
        confirmPassword: "",
      };
    },
    
    async changePassword(): Promise<void> {
        this.formErrors = {}; 
        try {
          const response = await fetch(`${this.getBaseURL()}current-user/`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.csrfToken,
            },
            credentials: "include",
            body: JSON.stringify({
              action: "change password",
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
/* General Page Styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

body {
  background: linear-gradient(to right, #1E3C72, #2A5298);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  text-align: center;
  padding: 20px;
}

.title {
  font-size: 3rem;
  color: #ff7f00;
  margin-bottom: 30px;
  font-weight: 700;
  text-align: center;
}

.error {
  color: #ff4d4d;
  font-weight: bold;
}

/* User Info & Hobbies Section */
.content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 30px;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.blob {
  background: rgba(255, 255, 255, 0.25);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 850px;
  backdrop-filter: blur(20px);
  color: black;
  text-align: left;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  margin: 0 auto;
}

.blob:hover {
  transform: scale(1.03);
  box-shadow: 0 18px 36px rgba(0, 0, 0, 0.5);
}

.blob h2 {
  margin-bottom: 15px;
  color: #ff7f00;
  font-size: 2rem;
}

.blob p {
  color: black;
  font-size: 1.1rem;
  font-weight: 500;
}

/* Form Styling */
.label {
  font-weight: bold;
  display: block;
  margin-top: 15px;
  color: black;
  font-size: 1.1rem;
}

.input {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  border: 1px solid rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.35);
  color: black;
  font-size: 1rem;
}

.input::placeholder {
  color: rgba(0, 0, 0, 0.7);
}

.input:focus {
  border-color: #ff9800;
  outline: none;
  background: rgba(255, 255, 255, 0.45);
  box-shadow: 0 0 12px rgba(255, 152, 0, 0.7);
}

/* Buttons */
button {
  padding: 14px 25px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1.1rem;
  transition: all 0.3s ease-in-out;
  outline: none;
  margin: 10px;
}

button:hover {
  transform: scale(1.07);
}

.save-btn, .edit-btn, .edit-btn-1 {
  background: linear-gradient(135deg, #ff9800, #ff5e00);
  color: white;
}

.cancel-btn, .close-request-modal {
  background: #ff4d4d;
  color: white;
}

.logout-btn {
  background: #d9534f;
  color: white;
}

.show-requests {
  background: #f39c12;
  color: white;
}

.add-btn, .accept {
  background: #28a745;
  color: white;
}

/* Hobbies Section */
.hobby-list {
  list-style: none;
  padding: 0;
}

.hobby-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.35);
  border-radius: 10px;
  margin: 8px 0;
  color: black;
}

/* Modal Styling */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content,
.modal-content-requests {
  background: rgba(255, 255, 255, 0.25);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
  width: 90%;
  max-width: 500px;
  text-align: center;
  color: black;
  backdrop-filter: blur(20px);
}

.modal-request-container {
  margin-top: 15px;
}

.no-requests {
  font-weight: bold;
  color: black;
}

/* Responsive Design */
@media (max-width: 768px) {
  .blob, .modal-content, .modal-content-requests {
    width: 95%;
  }
}

</style>


