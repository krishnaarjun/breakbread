<template>
  <div class="footer-bottom">
    <div class="copy-right">© 2003-2019 Inmar Inc.</div>
  </div>
</template>
<script>
export default {}
</script>
<style  lang="scss">
.footer-bottom {
  color: white;
  background-color: $footer-bg;
  font-size: 14px;
  font-weight: normal;
  text-align: left;
  overflow: hidden;
  height: $footer-height;
  display: flex;
  align-items: center;
  .copy-right {
    width: 200px;
    padding-left: $outer-spacer;
  }
}
</style>
