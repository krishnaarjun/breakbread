<template>
  <div>
    <Header/>
    <div class="container">
      <slot/>
    </div>
    <Footer/>
  </div>
</template>
<script>
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default {
  components: { Header, Footer }
}
</script>
<style lang="scss" scoped>
.container {
  min-height: calc(100vh - #{$footer-height});
  background: #edf1f5;
  padding-top: $header-height;
}
</style>
