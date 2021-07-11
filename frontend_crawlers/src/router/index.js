import Vue from "vue"
import VueRouter from "vue-router"

const DashboardLayout = () => import("../containers/DashboardLayout.vue")
const LinkedinGeneral = () => import("../views/Linkedin/General.vue")
const Profile = () => import("../views/Profile.vue")
const Accounts = () => import("../views/Accounts.vue")

Vue.use(VueRouter)
const routes = [
    {
        path: "/",
        name: "Dashboard",
        component: DashboardLayout,
        children: [
            {
                path: "/linkedin",
                name: "Linkedin General",
                component: LinkedinGeneral,
            },
            {
                path: "/profile",
                name: "Profile",
                component: Profile,
            },
            {
                path: "/accounts",
                name: "Accounts",
                component: Accounts,
            },
        ],
    },
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
})

export default router
