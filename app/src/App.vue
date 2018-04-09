<template>
  <div id="app">
    <nav-bar></nav-bar>
    <router-view/>
  </div>
</template>

<script>
  import NavBar from './components/NavBar.vue'

  export default {
    components: {NavBar},
    name: 'App'
  }
</script>

<style lang="scss">
  #app {
    font-family: Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

    header {
      padding: 1rem 1.5rem;
      margin-bottom: 1.5rem;
      background-color: #efefef;
      border-bottom: solid 0.1rem #d4d4d4;

      h1 {
        margin: 0;
        padding: 0;
        font-size: 2.4rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5rem;
      }
    }

    h2 {
      position: relative;
      font-size: 2rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.3rem;
      margin: 1.5rem;
      padding: 0;

      &:before {
        content: '';
        position: absolute;
        bottom: -1rem;
        left: 50%;
        width: 3rem;
        height: 0.2rem;
        background-color: #898989;
        transform: translateX(-50%);
      }
    }

    h3 {
      font-size: 1.8rem;
      font-weight: 600;
      padding: 0;
      margin: 1.5rem 0;
    }

    form {
      max-width: 40rem;
      margin: auto;
      font-size: 1.4rem;

      label {
        display: block;
        font-size: 1.4rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.2rem;
      }

      input {
        display: block;
        width: 100%;
        margin-bottom: 1.5rem;
        padding: 0.5rem 0.8rem;
        border: solid 0.1rem #d4d4d4;
        font-size: 1.4rem;
        outline: none;
      }
    }

    button {
      padding: 0.5rem 1rem;
      font-size: 1.3rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.2rem;
      background-color: #cdcdcd;
      color: #565656;
      border: solid 0.1rem #898989;
      cursor: pointer;

      &:hover {
        background-color: #dedede;
        color: #454545;
        border-color: #a4a4a4;
      }
    }

    table {
      font-size: 1.4rem;

      .consolidated-stat {
        font-size: 1.8rem;
        font-weight: 600;
      }

      .percentage-stat {
        color: #898989;
      }
    }
  }
</style>
