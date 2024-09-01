import { createRouter, createWebHistory } from "vue-router";
import Home from '@/components/HomePage.vue'
import ChatRoom from '@/components/ChatRoom.vue'
import SOS from '@/components/SOS.vue'
import UserPage from "@/components/UserPage.vue";


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },

    {
      path: '/ChatRoom',
      name: 'ChatRoom',
      component: ChatRoom
  },

  {
    path: '/SOS',
    name: 'SOS',
    component: SOS
},
{
    path: '/UserPage',
    name: 'UserPage',
    component: UserPage
},
   
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;