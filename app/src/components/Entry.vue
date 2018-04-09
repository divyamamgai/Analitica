<template>
  <div class="container">
    <div class="row">
      <div class="col-xs-12 col-sm-12 text-center">
        <h2>Welcome Admin</h2>
      </div>
    </div>
    <div class="row">
      <div class="col-xs-12 col-sm-6">
        <login-form></login-form>
      </div>
      <div class="col-xs-12 col-sm-6">
        <register-form></register-form>
      </div>
    </div>
  </div>
</template>

<script>
  import LoginForm from './LoginForm.vue'
  import RegisterForm from './RegisterForm.vue'

  export default {
    components: {
      RegisterForm,
      LoginForm
    },
    name: 'Entry',
    data () {
      return {}
    }
  }
</script>

<style scoped>
</style>
