<template>
  <div class="test-modal">
    <card title="User card">
      <div>
        <p> {{ userObj.email }} </p>
        <div class="col-10">
        <p>Select user role</p>
          <el-select
            class="select-default mb-3"
            style="width: 100%;"
            placeholder="Select campaign type"
            v-model="current_role"
          >
            <el-option
              class="select-default"
              v-for="role in roles"
              :key="role"
              :label="role"
              :value="role"
            ></el-option>
          </el-select>
        </div>

        <div class="col-10">
        <p>Change user password</p>
        <fg-input>
              <textarea
                class="form-control"
                placeholder="Enter New Password"
                rows="1"
                name="Password"
                v-model="password"
              ></textarea>
        </fg-input>
        </div>

        <div class="col-10">
        <p>Login as this user</p>
        <button
            type="submit"
            v-on:click="change_user"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Go ahead!</button>
        </div>

        <div class="col-12 d-flex flex-row-reverse">
          <button
            type="submit"
            v-on:click="submit"
            class="btn btn-outline btn-wd btn-success mx-1"
          >Save</button>
          <button
            v-on:click="discard"
            type="discard"
            class="btn btn-outline btn-wd btn-danger"
          >Discard</button>
        </div>

      </div>

    </card>
  </div>
</template>

<script>
import { Notification, Select, Option } from "element-ui";

import axios from "@/api/axios-auth";

const CHANGE_ROLES_API = "/admin/roles/change";
const CHANGE_USER_PASSWORD_API = "/admin/password/change";
const LOGIN_AS_USER_API = "/admin/login/as";


export default {
  components: {
    [Select.name]: Select,
    [Option.name]: Option,
  },
  props: {
    userObj: Object,
    roles: Array,
    valueUpdated: Function
  },
  data() {
    return {
        current_role: null,
        password: null,
    };
  },
  methods: {
    change_user() {
      const path = LOGIN_AS_USER_API;

      var data = new FormData();
      data.append("_user_id", this.userObj._id.$oid);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error changing user." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            localStorage.setItem('token', r.token); // maybe here we should call dispatch to catch Promises
            localStorage.setItem('role', this.userObj.role);

            this.$emit("close");
            this.$router.push('login');
            
            Notification.success({title: "Success", message: "User changed"});
          }
        })
        .catch(error => {
          var msg = "Error changing user. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    change_password() {
      const path = CHANGE_USER_PASSWORD_API;

      var data = new FormData();
      data.append("_user_id", this.userObj._id.$oid);
      data.append("_new_password", this.password);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error updating user password." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.valueUpdated(this.userObj);
            Notification.success({title: "Success", message: "User password changed"});
          }
        })
        .catch(error => {
          var msg = "Error updating user password. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    change_role() {
      const path = CHANGE_ROLES_API;

      var data = new FormData();
      data.append("_user_id", this.userObj._id.$oid);
      data.append("_new_role", this.current_role);

      axios
        .post(path, data)
        .then(res => {
          var r = res.data;
          if (r.code <= 0) {
            var msg = "Error updating user role." + r.msg;
            Notification.error({ title: "Error", message: msg });
          } else {
            this.valueUpdated(this.userObj);
            Notification.success({title: "Success", message: "User role changed"});
          }
        })
        .catch(error => {
          var msg = "Error updating user role. ERROR: " + error;
          Notification.error({ title: "Error", message: msg });
        });
    },
    submit() {
      if(this.password) {
          if(this.password.lengh < 8) {
            Notification.error({title: "Error", message: "Short password"});
            return;
          } else {
              this.change_password();
          }
      }

      if(this.current_role !== this.userObj.role && this.current_role !== null) {
          this.change_role();
      }
      
      this.$emit("close");
    },
    discard() {
      this.$emit("close");
    }
  },
  mounted() {
      this.current_role = this.userObj.role;
  }
};
</script>
<style>

</style>
  