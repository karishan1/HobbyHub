  <template>
    <div class="mainpage-container">
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
              <input
                type="password"
                v-model="passwordForm.oldPassword"
                class="input"
              />
              <label class="label">New Password:</label>
              <input
                type="password"
                v-model="passwordForm.newPassword"
                class="input"
              />
              <label class="label">Confirm New Password:</label>
              <input
                type="password"
                v-model="passwordForm.confirmPassword"
                class="input"
              />
              <button @click="changePassword" class="save-btn">Change Password</button>
              <button @click="cancelPasswordChange" class="cancel-btn">Cancel</button>
            </div>

            <div v-else>
              <label class="label">Username:</label>
              <input
                type="text"
                v-model="editedUser.username"
                class="input"
              />
              <p v-if="formError" class="form-error">{{ formError }}</p>

              <label class="label">Email:</label>
              <input
                type="email"
                v-model="editedUser.email"
                class="input"
              />
              <label class="label">DOB:</label>
              <input
                type="date"
                v-model="editedUser.DOB"
                class="input"
              />
              <button @click="saveDetails" class="save-btn">Save</button>
              <button @click="cancelEdit" class="cancel-btn">Cancel</button>
              <button @click="togglePasswordChange" class="edit-btn">Change Password</button>
            </div>
          </div>

          <!-- Display User Info -->
          <div v-else>
            <p><span class="label">Username:</span> {{ userStore.username }}</p>
            <p><span class="label">Email:</span> {{ user.email }}</p>
            <p><span class="label">DOB:</span> {{ user.DOB }}</p>
            <button @click="editDetails" class="edit-btn">Edit Details</button>
          </div>
        </div>

        <!-- Hobbies Blob -->
        <div class="blob hobbies">
          <h2>Hobbies</h2>
          <ul class="hobby-list">
            <li v-for="hobby in user.hobbies" :key="hobby" class="hobby-item">
              {{ hobby }}
            </li>
          </ul>
        </div>
      </div>

      <div v-else class="loading">
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
        title: "User Dashboard",
        user: {
          username: "",
          email: "",
          DOB: "",
          hobbies: [],
        },
        editedUser: {},
        passwordForm: {
          oldPassword: "",
          newPassword: "",
          confirmPassword: "",
        },
        isEditing: false,
        isChangingPassword: false,
        error: null,
        formError: null,
      };
    },
    computed: {
        userStore(){
            return useUserStore();
        }
    },
    methods: {
      fetchUser() {  // Fetches current user data
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
      editDetails() {
        this.editedUser = { ...this.user }; // Clones the user details
        this.isEditing = true;
      },

      async isUsernameTaken(username) {
        try {
          const response = await fetch("http://127.0.0.1:8000/user_list/", {
            method: "GET",
            credentials: "include",
          });

          if (response.ok) {
            const users = await response.json();
            return users.some((user) => user.username === username && user.username !== this.user.username);
          } else {
            console.error("Failed to fetch user list.");
            return false;
          }
        } catch (error) {
          console.error("An error occurred:", error);
          return false;
        }
      },

      async saveDetails() {
        try {
          this.formError = null;

          const isTaken = await this.isUsernameTaken(this.editedUser.username);
          if (isTaken) {
            this.formError = "Username is already taken.";
            return;
          } 

          const response = await fetch("http://127.0.0.1:8000/api/current-user/", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(this.editedUser),
          });

          if (response.ok) {
            console.log("User details updated successfully!");
            this.isEditing = false;
            this.formError = null;
            this.fetchUser();
          } else {
            const errorResponse = await response.json();
            this.formError = errorResponse.error || "Failed to update user.";
          }
        } catch (error) {
          this.formError = "An unexpected error occurred.";
        }
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
      changePassword() {
      
      },
      cancelEdit() {
        this.isEditing = false;
        this.isChangingPassword = false;
      },
    },
    created() {
      this.fetchUser();
    },
  };
  </script>


  <style scoped>
  /* Main Container */
  .mainpage-container {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 1rem;
    font-family: Arial, sans-serif;
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
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .hobby-item {
    background: #ffebcd;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    color: #333;
    font-weight: bold;
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
  </style>
