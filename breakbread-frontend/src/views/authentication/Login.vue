<template>
  <div>
    <Card class="login-card">
      <h3 class="header">Login</h3>
      <Divider size="small" class="divider"/>
      <Form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @submit.native.prevent="handleSubmit('loginForm')"
      >
        <FormItem label="Email" prop="email">
          <Input type="text" v-model="loginForm.email" size="large" placeholder="Enter your email"></Input>
        </FormItem>
        <FormItem label="password" prop="password" class="mb-10">
          <Input
            type="password"
            v-model="loginForm.password"
            size="large"
            placeholder="Enter you password"
          ></Input>
        </FormItem>
        <br>
        <input
          type="submit"
          style="position: absolute; left: -9999px; width: 1px; height: 1px;"
          tabindex="-1"
        >
        <FormItem class="text-center">
          <Button
            type="primary"
            :loading="loginLoading"
            v-on:click="handleSubmit('loginForm')"
            size="large"
            long
          >
            <span v-if="!loginLoading">Sign In</span>
            <span v-else>Processing...</span>
          </Button>
        </FormItem>
      </Form>
    </Card>
  </div>
</template>
<script>
import auth from '@/services/auth'
import router from '@/main'

export default {
  data () {
    const validateEmail = (rule, value, callback) => {
      let emailPattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if (value === '') {
        callback(new Error('Enter you email'))
      } else {
        if (!emailPattern.test(String(value).toLowerCase())) {
          callback(new Error('Please enter valid email'))
        }
        callback()
      }
    }
    return {
      loginLoading: false,
      loginForm: {
        email: '',
        password: ''
      },
      loginRules: {
        email: [{ validator: validateEmail, trigger: 'blur', required: true }],
        password: [
          {
            required: true,
            message: 'Please fill in the password.',
            trigger: 'blur'
          },
          {
            type: 'string',
            min: 6,
            message: 'The password length cannot be less than 6 bits',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      let that = this
      let credentials = JSON.parse(JSON.stringify(this.loginForm))
      this.$refs[name].validate(valid => {
        if (valid) {
          auth
            .login(credentials)
            .then(data => {
              router.go('/')
            })
            .catch(error => {
              that.$Notice.error({
                title: 'Error Login',
                desc: error
              })
              console.log(error)
            })
        } else {
          that.$Notice.error({
            title: 'Invalid Form',
            desc: 'Please enter valid email and password'
          })
        }
      })
    }
  }
}
</script>
<style lang="scss">
.route-content {
  padding-top: 1px;
  margin-top: -1px;
}
.login-card {
  width: 23vw;
  margin: auto;
  height: initial;
  margin-top: 50px;
  min-width: 385px;
  .divider {
    background-color: $info;
  }
  .header {
    font-size: 1.5em;
    text-align: center;
    margin: 5px;
  }
  .ivu-form-item-label {
    font-size: 1.1em;
  }
  .ivu-btn {
    span {
      font-size: 1.1em;
    }
  }
}
</style>
