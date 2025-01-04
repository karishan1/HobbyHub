import { defineStore } from "pinia";

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user_id: null as string | null,
        username: null as string | null,
        hobbies: [] as string[],
    }),
    actions: {
        setUser(userId: string, username: string, hobbies: string[]){
            this.user_id = userId;
            this.username = username;
            this.hobbies = hobbies;

            localStorage.setItem('user', JSON.stringify(this.$state));
        },
        loadUser() {
            const user = localStorage.getItem('user');
            if (user){
                const parsedUser = JSON.parse(user);
                this.user_id = parsedUser.userId;
                this.username = parsedUser.username;
                this.hobbies = parsedUser.hobbies;

            }
        },
        clearUser(){
            this.user_id = null;
            this.username = null;
            this.hobbies = [];
        }
    }
})
