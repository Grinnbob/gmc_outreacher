import Vue from "vue"
import VueRouter from "vue-router"

const DashboardLayout = () => import("../containers/DashboardLayout.vue")

const LinkedinGeneral = () => import("../views/Linkedin/General.vue")
const LinkedinSearchSN = () => import("../views/Linkedin/Search_sn.vue")

const Profile = () => import("../views/Profile.vue")
const Accounts = () => import("../views/Accounts.vue")
const AccountAdd = () => import("../views/AccountAdd.vue")
const Actions = () => import("../views/Actions.vue")

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
                path: "/linkedin/sn/search",
                name: "Linkedin search SN",
                component: LinkedinSearchSN,
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
            {
                path: "/account/add",
                name: "Add account",
                component: AccountAdd,
            },
            {
                path: "/actions",
                name: "Actions",
                component: Actions,
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