<template>
  <nav class="navbar navbar-expand-lg ">
    <div class="container-fluid">
      <div class="navbar-minimize">
        <button class="btn btn-outline btn-fill btn-round btn-icon d-none d-lg-block" @click="minimizeSidebar">
          <i :class="$sidebar.isMinimized ? 'fa fa-ellipsis-v' : 'fa fa-navicon'"></i>
        </button>
      </div>
      <a class="navbar-brand">{{this.$route.name}}</a>
      <button type="button"
              class="navbar-toggler navbar-toggler-right"
              :class="{toggled: $sidebar.showSidebar}"
              aria-expanded="false"
              @click="toggleSidebar">
        <span class="navbar-toggler-bar burger-lines"></span>
        <span class="navbar-toggler-bar burger-lines"></span>
        <span class="navbar-toggler-bar burger-lines"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end">
        <ul class="navbar-nav">
          <drop-down position="right">
            <i slot="title" class="nc-icon nc-bullet-list-67"></i>
            <a class="dropdown-item" href="/help">
              <i class="nc-icon nc-umbrella-13"></i> Help Center
            </a>
            <div class="dropdown-item text-danger">
              <button type="button" @click.prevent="onLogout" class="btn btn-fill btn-info btn-round btn-wd">Logout</button>
            </div>

          </drop-down>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  export default {
    computed: {
      routeName () {
        const {name} = this.$route
        return this.capitalizeFirstLetter(name)
      }
    },
    data () {
      return {
        activeNotifications: false
      }
    },
    methods: {
      capitalizeFirstLetter (string) {
        return string.charAt(0).toUpperCase() + string.slice(1)
      },
      toggleNotificationDropDown () {
        this.activeNotifications = !this.activeNotifications
      },
      closeDropDown () {
        this.activeNotifications = false
      },
      toggleSidebar () {
        this.$sidebar.displaySidebar(!this.$sidebar.showSidebar)
      },
      hideSidebar () {
        this.$sidebar.displaySidebar(false)
      },
      minimizeSidebar () {
        this.$sidebar.toggleMinimize()
      },

      onLogout(){
        var _this = this;
        this.$store.dispatch('auth/logout').then(
          resolve => {
            _this.$router.push("login");
          },
          reject => {
            console.log("error here: ", reject);
          }
        )
        .catch(err => {
          console.error("login error: ", err);
        });
    },

    }
  }

</script>
<style>

</style>
