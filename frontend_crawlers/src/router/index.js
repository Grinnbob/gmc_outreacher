import Vue from "vue"
import VueRouter from "vue-router"

Vue.use(VueRouter)

// Layouts
const DashboardLayout = () => import("../containers/DashboardLayout.vue")
const AuthLayout = () => import("../views/Auth/AuthLayout.vue")

// Auth
const Login = () => import("../views/Auth/Login.vue")
const Register = () => import("../views/Auth/Register.vue")

// General
const Profile = () => import("../views/General/Profile.vue")
const Accounts = () => import("../views/General/Accounts.vue")
const AccountAdd = () => import("../views/General/AccountAdd.vue")
const Actions = () => import("../views/General/Actions.vue")
const Guide = () => import("../views/General/Guide.vue")
const Docs = () => import("../views/General/Docs.vue")

// Admin
const AdminUsers = () => import("../views/Admin/Users.vue")

// Linkedin navigation
const navigateLinkedinGeneral = () =>
    import("../views/Linkedin/General/General.vue")
const navigateLinkedin = () => import("../views/Linkedin/General/Linkedin.vue")
const navigateLinkedinSN = () =>
    import("../views/Linkedin/General/Linkedin_sn.vue")

// Actions Linkedin
const LinkedinSearch = () => import("../views/Linkedin/Search.vue")
const LinkedinSearchSscribe = () =>
    import("../views/Linkedin/Search_scribe.vue")
const LinkedinScribe = () => import("../views/Linkedin/Scribe.vue")

// Actions Linkedin SN
const LinkedinSearchSN = () => import("../views/Linkedin/Search_sn.vue")
const LinkedinSearchSscribeSN = () =>
    import("../views/Linkedin/Search_scribe_sn.vue")
const LinkedinScribeSN = () => import("../views/Linkedin/Scribe_sn.vue")

const routes = [
    {
        path: "/",
        name: "Auth",
        redirect: "/login",
        component: AuthLayout,
        children: [
            {
                path: "/login",
                name: "Login",
                component: Login,
            },
            {
                path: "/register",
                name: "Register",
                component: Register,
            },
        ],
    },
    {
        path: "/",
        name: "Admin",
        component: DashboardLayout,
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: "/admin/users",
                name: "Admin Users",
                component: AdminUsers,
            },
        ],
    },
    {
        path: "/",
        name: "Dashboard",
        component: DashboardLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: "/guide",
                name: "Guide",
                component: Guide,
            },
            {
                path: "/docs",
                name: "Docs",
                component: Docs,
            },
            {
                path: "/linkedin",
                name: "Linkedin General",
                component: navigateLinkedinGeneral,
            },
            {
                path: "/navigate/linkedin",
                name: "Linkedin General",
                component: navigateLinkedin,
            },
            {
                path: "/navigate/linkedin/sn",
                name: "Linkedin General",
                component: navigateLinkedinSN,
            },
            {
                path: "/linkedin/sn/scribe",
                name: "Linkedin SN scribe profile",
                component: LinkedinScribeSN,
            },
            {
                path: "/linkedin/sn/search",
                name: "Linkedin search SN",
                component: LinkedinSearchSN,
            },
            {
                path: "/linkedin/sn/search/scribe",
                name: "Linkedin search scribe SN",
                component: LinkedinSearchSscribeSN,
            },
            {
                path: "/linkedin/scribe",
                name: "Linkedin scribe profile",
                component: LinkedinScribe,
            },
            {
                path: "/linkedin/search",
                name: "Linkedin search",
                component: LinkedinSearch,
            },
            {
                path: "/linkedin/search/scribe",
                name: "Linkedin search scribe",
                component: LinkedinSearchSscribe,
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

router.beforeEach((to, from, next) => {
    let token = localStorage.getItem("token")
    let role = localStorage.getItem("role")

    let requireAuth = to.matched.some((record) => record.meta.requiresAuth)
    let requireAdmin = to.matched.some((record) => record.meta.requiresAdmin)

    if (requireAuth && !token) {
        next("/login")
    } else if (token && (to.path == "/login" || to.path == "/register")) {
        next("/guide")
    } else if (requireAdmin && role != 3) {
        // string here, 3 = admin, 2 = api user, 1 = common user
        next("/guide")
    } else {
        next()
    }
})

export default router
