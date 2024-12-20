import { defineStore } from "pinia";

export const UserStore = defineStore('userStore',{
    state: () => ({
        user_id: null as string | null,
    }),
    actions: {
        setUserId(id : string){
            this.user_id = id;
            sessionStorage.setItem('user_id',id);
        },
        getUserIdFromSession(){
            const id = sessionStorage.getItem('user_id')
            if (id){
                this.user_id = id;
            }
        },
        clearUserId(){
            this.user_id = null;
            sessionStorage.removeItem('user_id');
        },
    },
},);