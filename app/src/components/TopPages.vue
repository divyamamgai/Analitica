<template>
  <div>
    <h3>Top Pages</h3>
    <table class="table table-bordered">
      <thead>
      <tr>
        <th>Page</th>
        <th>Count</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td class="text-right" colspan="2">
          <span class="consolidated-stat" title="Total Visits">
            {{ $parent.consolidated.visits }}
            <small> visits in total</small>
          </span>
        </td>
      </tr>
      <tr v-for="page in pages">
        <td>{{ page.url }}</td>
        <td class="text-right">
          {{ page.total }}
          <small class="percentage-stat">
            ({{ (page.total / $parent.consolidated.visits).toFixed(2) * 100 }}%)
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
    name: 'TopPages',
    data () {
      return {
        pages: []
      }
    },
    mounted () {
      this.getPages()
    },
    methods: {
      getPages () {
        Analytics.topPages()
          .then((pages) => {
            this.pages = pages
          })
      }
    }
  }
</script>

<style scoped>
</style>
