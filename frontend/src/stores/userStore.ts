import { defineStore } from "pinia";

interface UserState {
    user_id: number | null;
    username: string | null;
    hobbies: string[];
}

export const useUserStore = defineStore('userStore', {
    state: (): UserState => ({
        user_id: null,
        username: null,
        hobbies: [],
    }),
    actions: {
        setUser(userId: number, username: string, hobbies: string[]): void {
            this.user_id = userId;
            this.username = username;
            this.hobbies = hobbies;
            localStorage.setItem('user', JSON.stringify(this.$state));
        },
        loadUser(): void {
            const user = localStorage.getItem('user');
            if (user){
                const parsedUser = JSON.parse(user);
                this.user_id = parsedUser.userId;
                this.username = parsedUser.username;
                this.hobbies = parsedUser.hobbies;
            }
        },
        clearUser(): void {
            this.user_id = null;
            this.username = null;
            this.hobbies = [];
        }
    }
})
