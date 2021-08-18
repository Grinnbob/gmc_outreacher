<template>
    <div>
        <b-navbar toggleable="md" type="light" variant="light">
            <b-navbar-brand href="/guide">
                <img src="../../public/logo.png" />
            </b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-navbar-nav>
                <b-nav-item href="/linkedin" class="text">LinkedIn</b-nav-item>
                <b-nav-item
                    href="https://linkedin.devlabsco.com/api-docs/"
                    target="blank"
                    class="text"
                    >API</b-nav-item
                >
                <b-nav-item href="/docs" class="text">Docs</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto" v-if="role == 3">
                <b-nav-item-dropdown text="Admin" right>
                    <b-dropdown-item href="/admin/users">Users</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>

            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown text="Settings" right>
                    <b-dropdown-item href="/profile">Profile</b-dropdown-item>
                    <b-dropdown-item href="/accounts">Accounts</b-dropdown-item>
                    <!-- <b-dropdown-item href="/actions">Actions</b-dropdown-item> -->
                    <b-dropdown-item href="#">Billing</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-navbar>

        <div class="mx-4 my-4">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            role: null,
        }
    },
    mounted() {
        this.role = localStorage.getItem("role")
    },
}
</script>
<style>
.text {
    color: #0373b2;
    font-size: 20px;
}
</style>
