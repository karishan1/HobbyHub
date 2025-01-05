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
            <input type="text" v-model="editedUser.username" class="input" />
            <p v-if="formError" class="form-error">{{ formError }}</p>

            <label class="label">Email:</label>
            <input type="email" v-model="editedUser.email" class="input" />
            <label class="label">DOB:</label>
            <input type="date" v-model="editedUser.DOB" class="input" />
            <button @click="saveDetails" class="save-btn">Save</button>
            <button @click="cancelEdit" class="cancel-btn">Cancel</button>
            <button @click="togglePasswordChange" class="edit-btn">Change Password</button>
          </div>
        </div>

        <!-- Display User Info -->
        <div v-else>
          <p><span class="label">Username:</span> {{ user.username }}</p>
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
            <button @click="removeHobby(hobby)" class="remove-btn">X</button>
          </li>
        </ul>
        <button @click="showHobbiesModal = true" class="edit-btn">Edit Hobbies</button>
      </div>
    </div>

    <div v-if="showHobbiesModal" class="modal">
      <div class="modal-content">
        <h4>Add a New Hobby to the Database</h4>
        <input v-model="newHobbyName" placeholder="Type new hobby name..." />
        <button @click="addNewHobby" class="add-btn">Add Hobby</button>

        <h4>Available Hobbies</h4>
        <ul>
          <li v-for="hobby in availableHobbies" :key="hobby.id" class="hobby-item">
            {{ hobby.hobby_name }}
            <button @click="addExistingHobby(hobby.id)" class="add-btn">Add</button>
          </li>
        </ul>

        <button @click="showHobbiesModal = false" class="cancel-btn">Close</button>
      </div>
    </div>

    <div v-else class="loading">
      <p>Loading user data...</p>
    </div>
  </div>
</template>

<script lang="ts">
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

export default defineComponent({
  name: "MainPage",

  data() {
    return {
      title: "User Dashboard",
      user: {} as User,
      editedUser: {} as User,
      availableHobbies: [] as Hobby[],
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
    };
  },
  methods: {
    async fetchUser() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/current-user/", {
          method: "GET",
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.user = await response.json();
      } catch (error) {
        this.error = error instanceof Error ? error.message : String(error);
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
        const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || "";

        const response = await fetch("http://127.0.0.1:8000/add_user_hobby/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
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
        }

        alert("Hobby added successfully!");
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
        const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || "";

        const response = await fetch("http://127.0.0.1:8000/add_hobby_to_db/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ hobby_name: this.newHobbyName }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to add new hobby to the database: ${response.status}`);
        }

        alert("Hobby added to the database successfully!");
        this.newHobbyName = "";
        await this.fetchHobbies();
      } catch (error) {
        console.error("Error adding new hobby to the database:", error);
      }
    },

    async removeHobby(hobbyName: string) {
      try {
        const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/)?.[1] || "";

        const response = await fetch("http://127.0.0.1:8000/remove_user_hobby/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({ hobby_name: hobbyName }),
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to remove hobby: ${response.status}`);
        }

        this.user.hobbies = this.user.hobbies.filter((hobby) => hobby !== hobbyName);

        alert("Hobby removed successfully!");
      } catch (error) {
        console.error("Error removing hobby:", error);
      }
    },

    editDetails() {
      this.editedUser = { ...this.user };
      this.isEditing = true;
    },

    async saveDetails() {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/current-user/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(this.editedUser),
        });

        if (!response.ok) {
          throw new Error("Failed to update user details.");
        }

        this.isEditing = false;
        this.fetchUser();
        alert("User details updated successfully!");
      } catch (error) {
        this.formError = error instanceof Error ? error.message : String(error);
      }
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
      // Implement the password change logic here
      // For example, you might want to send a request to the server
      // to update the user's password using the values in passwordForm.
    },
  },
  created() {
    this.fetchUser();
    this.fetchHobbies();
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
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}

.hobby-item {
  display: flex;
  align-items: center;
  background: #ffebcd;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
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


</style>
