<template>
  <div class="outer-container">
    <Header/>
    <div class="container">
      <div class="content">
        <slot/>
      </div>
      <div class="sidebar">
        <Sidebar/>
      </div>
    </div>
  </div>
</template>
<script>
import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'
export default {
  components: { Header, Sidebar }
}
</script>
<style lang="scss">
.outer-container {
  background: #edf1f5;
  overflow: hidden;
  .container {
    min-height: 100vh;
    position: relative;
    margin: auto;
    padding-top: 1px;
    margin-top: -1px;
    .content {
      margin: $header-height 0 0 $sidebar-width;
      overflow: auto;
      .content-inner {
        padding: $outer-spacer 50px;
        overflow: auto;
      }
    }
    .sidebar {
      position: fixed;
      width: $sidebar-width;
      left: 0px;
      top: $header-height;
      bottom: 0px;
      background-color: white;
      z-index: 90;
      border-top: 1px solid  $border;
    }
  }
}
</style>
