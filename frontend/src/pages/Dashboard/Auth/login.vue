<template>
  <auth-layout pageClass="login-page">
    <div class="row d-flex justify-content-center align-items-center">
      <div class="col-lg-4 col-md-6 col-sm-8">
        <form method="#" action="#">
          <!--You can specify transitions on initial render. The `card-hidden` class will be present initially and then it will be removed-->
          <card>
            <div slot="header">
              <h3 class="card-title text-center">Login</h3>
            </div>

            <pulse-loader :loading="loading" :color="color"></pulse-loader>

            <div v-if="!loading">
              <div class="row">
                <div class="col-12 mb-3">
                  <label class="text">email</label>
                  <el-input
                    label="Email address"
                    placeholder="Enter email"
                    type="email"
                    v-model="model.email"
                  ></el-input>
                </div>
              </div>

              <div class="row">
                <div class="col-12 mb-3">
                  <label class="text">password</label>
                  <el-input
                    label="passsword"
                    type="password"
                    placeholder="Password"
                    v-model="model.password"
                    show-password
                  ></el-input>
                </div>
              </div>

              <div v-if="error" class="form-group">
                <small class="text-danger">{{ error }}</small>
              </div>

              <div class="text-center">
                <button
                  type="submit"
                  @click.prevent="onSubmit"
                  class="btn btn-fill btn-info btn-round btn-wd"
                >Login</button>
                <br />
              </div>
            </div>

          </card>
        </form>
      </div>
    </div>
  </auth-layout>
</template>
<script>
import {
  Checkbox as LCheckbox,
  FadeRenderTransition
} from "src/components/index";

const AuthLayout = () => import("./AuthLayout.vue");
import { PulseLoader } from "vue-spinner/dist/vue-spinner.min.js";
import { mapGetters } from "vuex";

export default {
  components: {
    PulseLoader,
    LCheckbox,
    FadeRenderTransition,
    AuthLayout
  },
  computed: {
    ...mapGetters("auth", {
      // map `this.doneCount` to `this.$store.getters.doneTodosCount`
      error: "getLoginError",
      isAuth: "isAuthenticated"
    })
  },
  data() {
    return {
      loading: false,
      color: "#a7a7ff",

      model: {
        email: "",
        password: ""
      }
    };
  },
  methods: {
    toggleNavbar() {
      document.body.classList.toggle("nav-open");
    },
    closeMenu() {
      document.body.classList.remove("nav-open");
      document.body.classList.remove("off-canvas-sidebar");
    },
    onSubmit() {
      var _this = this
      this.loading = true
      
      this.$store
        .dispatch("auth/login", this.model)
        .then(
          resolve => {
            _this.$router.push("profile")
            _this.loading = false
          },
          reject => {
            console.log("error here: ", reject)
            _this.loading = false
          }
        )
        .catch(err => {
          console.error("login error: ", err)
          _this.loading = false
        });
    }
  },
  beforeDestroy() {
    this.closeMenu()
  }
};
</script>
<style>
.navbar-nav .nav-item p {
  line-height: inherit;
  margin-left: 5px;
}
.text {
  display: flex;
  font-size: 12px;
  font-weight: 200;
  line-height: 30px;
  text-transform: uppercase;
  color: rgb(119, 119, 119);
}
</style>
