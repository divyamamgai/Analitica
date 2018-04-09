<template>
  <div>
    <h3>Top Browsers</h3>
    <table class="table table-bordered">
      <thead>
      <tr>
        <th>Browser</th>
        <th>Version</th>
        <th>Count</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="text-right" colspan="3">
          <span class="consolidated-stat" title="Total Browsers">
            {{ $parent.consolidated.browsers }}
            <small> browsers in total</small>
          </span>
        </td>
      </tr>
      <tr v-for="browser in browsers">
        <td>{{ browser.name }}</td>
        <td>{{ browser.version }}</td>
        <td class="text-right">
          {{ browser.total }}
          <small class="percentage-stat">
            ({{ (browser.total / $parent.consolidated.visits).toFixed(2) * 100 }}%)
          </small>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { Analytics } from '../service'

  export default {
    components: {},
    name: 'TopBrowsers',
    data () {
      return {
        browsers: []
      }
    },
    mounted () {
      this.getBrowsers()
    },
    methods: {
      getBrowsers () {
        Analytics.topBrowsers()
          .then((browsers) => {
            this.browsers = browsers
          })
      }
    }
  }
</script>

<style scoped>
</style>
