<template>
  <div>
    <card>
      <div class="container">
          <div class="row">
              <div class="col-4 d-flex align-self-center">
                  <h3>
                  <i class="nc-icon nc-circle-09"></i> Profile
                  </h3>
              </div>
              <div class="col-8 d-flex flex-row-reverse align-self-center">
                  <button
                      @click.prevent="change_password"
                      type="button"
                      class="btn btn-default btn-success mx-1"
                  >Change password</button>
                  <button
                      @click.prevent="onLogout"
                      type="button"
                      class="btn btn-default btn-success mx-1"
                  >Logout</button>
              </div>
          </div>
      </div>
    </card>

    <card>
      <card>
        <p class="info">E-mail</p>
        <p>{{ user_data.email }}</p>
        <div v-if="user_data.role == 'admin'">
          <p class="info">Role</p>
          <p>{{ user_data.role }}</p>
        </div>
        <p class="info">Bonus code for friends</p>
        <p>{{ user_data.invite_code }}</p>
      </card>

    </card>

    <modals-container/>
  </div>

</template>
<script>
import axios from "@/api/axios-auth";
import { Notification, Select, Option } from "element-ui";

const Change_password_modal = () => import('./change_password_modal.vue')

const PROFILE_API_LIST = '/profile';

export default {
  data() {
    return {
      user_data: {}
    };
  },
  methods: {
    change_password() {
      this.$modal.show(
        Change_password_modal,
        {
          valueUpdated: newValue => {
          }
        },
        {
          width: "400",
          height: "auto",
          scrollable: true
        }
      );
    },
    onLogout() {
      var _this = this;
      this.$store.dispatch("auth/logout").then(
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
    loadUser() {
      const path = PROFILE_API_LIST;

      var data = new FormData();

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error loading user." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.user_data = JSON.parse(r.user);
            //console.log('user: ', this.user_data)
          }
        })
        .catch(error => {
          var msg = "Error loading lists. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    }
  },
  async mounted() {
    await this.loadUser();
    //console.log(this.user_data)
  },
  created() {
  }
};
</script>
<style>
.card_title {
  text-align: center;
  font-size: 35px;
  font-weight: 500;
}
.info {
  font-size: 20px;
  font-weight: 600;
  height: 10px;
}
</style>
