<template>
  <div class="header-wrapper">
    <div class="logo" :class="{ 'active': isPublic == false}">
      <router-link to="/">
        <img src="@/assets/images/logo.png">
      </router-link>
    </div>
    <div class="menu-spacer">
      <div class="action-menu-container" v-if="isPublic == false">
        <Avatar class="user-avatar">{{userinfo.username[0]}}</Avatar>
        <Dropdown trigger="click" placement="bottom-end">
          <a href="javascript:void(0)">
            {{userinfo.username}}
            <Icon type="ios-arrow-down"></Icon>
          </a>
          <DropdownMenu slot="list">
            <DropdownItem>
              <a href="javascript:void(0)" @click="logout()">Logout</a>
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </div>
  </div>
</template>
<script>
import auth from '@/services/auth'
export default {
  data () {
    return {
      userinfo: {},
      authenticated: false,
      isPublic: true
    }
  },
  methods: {
    logout () {
      auth.logout()
    }
  },
  mounted () {},

  beforeMount () {
    this.isPublic = !!this.$route.meta.isPublic
    auth.checkAuth()
    this.authenticated = auth.user.authenticated
    if (this.authenticated) {
      this.userinfo = auth.getUserInfo()
    }
  }
}
</script>
<style lang="scss">
.header-wrapper {
  position: fixed;
  top: 0px;
  width: 100%;
  z-index: 100;
  background-color: #fbb862;
  height: $header-height;
  display: flex;
  align-items: center;
  .logo {
    position: relative;
    text-align: left;
    display: inline-block;
    height: inherit;
    width: $sidebar-width;
    &.active {
      background: white;
    }
    a {
      display: block;
      height: inherit;
      padding: 6px $outer-spacer;
      img {
        height: 100%;
      }
    }
  }
  .menu-spacer {
    width: calc(100% - #{$sidebar-width});
    padding-right: $outer-spacer;
    height: 100%;
    display: inline-block;
    float: right;
    .action-menu-container {
      float: right;
      .user-avatar {
        color: #f56a00;
        background-color: #fde3cf;
        margin-right: 10px;
      }
      .ivu-dropdown {
        margin-top: 15px;
        font-size: 18px;
        .ivu-dropdown-rel {
          a {
            color: white;
          }
        }
        .ivu-select-dropdown {
          .ivu-dropdown-item {
            a {
              color: gray;
            }
          }
        }
      }
    }
  }
}
</style>
