<template>
  <div class="sidebar-container">
    <div class="nav-container">
      <div class="nav-item">
        <router-link to="/" class="nav-link">
          <Icon type="ios-clipboard-outline"/>Survey List
        </router-link>
      </div>
      <div class="nav-item">
        <router-link to="/groups" class="nav-link">
          <Icon type="ios-contacts-outline"/>Groups
        </router-link>
      </div>
      <div class="nav-item">
        <router-link to="/potlucks" class="nav-link">
          <Icon type="ios-basket-outline" />Potlucks
        </router-link>
      </div>
      <div class="nav-item">
        <router-link to="/food-list" class="nav-link">
          <!-- <Icon type="ios-pizza-outline" /> -->
          <Icon type="ios-restaurant-outline" />Foods
        </router-link>
      </div>
    </div>
  </div>
</template>
<style lang="scss">
.sidebar-container {
  .nav-container {
    .nav-item {
      margin-top: 2px;
      .nav-link {
        padding: 0.675rem 1.5rem;
        font-size: 0.875rem;
        display: block;
        color: rgba(0, 0, 0, 0.6);
        &.router-link-exact-active {
          margin-right: 0.5rem;
          margin-left: 0.5rem;
          padding-right: 1rem;
          padding-left: 1rem;
          border-radius: 0.375rem;
          background: #f6f9fc;
          color: rgba(0, 0, 0, 0.9);
        }
      }
      .ivu-icon {
        font-size: 1.5rem;
        margin-right: 10px;
      }
    }
  }
}
</style>
