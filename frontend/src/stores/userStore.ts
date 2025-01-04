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
        },
        clearUser(){
            this.user_id = null;
            this.username = null;
            this.hobbies = [];

        }
    }
})
