<template>
  <div>
    <h3>Top Screen Resolutions</h3>
    <table class="table table-bordered">
      <thead>
      <tr>
        <th>Screen Resolution</th>
        <th>Count</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="text-right" colspan="2">
          <span class="consolidated-stat" title="Total Browsers">
            {{ $parent.consolidated.screen_resolutions }}
            <small> screen resolutions in total</small>
          </span>
        </td>
      </tr>
      <tr v-for="screenResolution in screenResolutions">
        <td>{{ screenResolution.value }}</td>
        <td class="text-right">
          {{ screenResolution.total }}
          <small class="percentage-stat">
            ({{ (screenResolution.total / $parent.consolidated.visits).toFixed(2) * 100 }}%)
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
    name: 'TopScreenResolutions',
    data () {
      return {
        screenResolutions: []
      }
    },
    mounted () {
      this.getScreenResolutions()
    },
    methods: {
      getScreenResolutions () {
        Analytics.topScreenResolutions()
          .then((screenResolutions) => {
            this.screenResolutions = screenResolutions
          })
      }
    }
  }
</script>

<style scoped>
</style>
