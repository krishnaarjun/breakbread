<template>
  <div class="card">
    <div class="card-header">
      <Row>
        <Col span="3">
        <div class="name-avatar" v-bind:style="group.group_meta_data.avatar_gradient"> {{group.name[0]}}</div>
        </Col>
        <Col span="12">
        <span class="group-name">{{group.name}}</span>
        <!-- <span class="total-users-count">{{group.results.length}}</span> -->
        </Col>
        <Col span="9" class="text-right" v-if="group.status == 'locked'">
          <Icon type="ios-unlock" class="potluck-action potluck-action--unlock" @click="unlockPotluck(group.id)"/>
          <Button type="info" icon="md-checkbox-outline" @click="publishPotluck(group)" style="padding: 2px 8px">
            <span>Publish</span>
          </Button>
        </Col>
        <Col span="9" class="text-right" v-if="group.status == 'published'">
          <!-- <Icon type="ios-unlock" class="potluck-action potluck-action--unlock"/> -->
          <div class="potluck-date-info">{{group.hosting_on | formatDate}}</div>
        </Col>
        <Col span="9" class="text-right" v-if="group.isManagerAssigned">
        <!-- <Button :size="buttonSize" type="dashed">Lock-In</Button> -->
        <!-- <Icon type="ios-unlock-outline" /> -->
        <!-- <Icon type="ios-unlock"/> -->
          <Icon type="ios-undo" @click="undoManager(group)"  class="potluck-action potluck-action--undo" style="font-size: 18px; padding: 5px; margin-right: 5px; color: gray; cursor: pointer;" />
          <Button type="info" icon="ios-unlock" @click="lockGroup(group)" style="padding: 2px 8px">
            <span>Lock-In</span>
            <!-- <span v-else>Loading...</span> -->
          </Button>
        </Col>
      </Row>
      <Row class="ethnicity-container code-row-bg" type="flex" justify="space-between">
        <Col span="13">
        <div class="ethnicity-count">
          <Icon type="md-arrow-up"/>
          {{group.black_or_african_american}}%
        </div>
        <div class="ethnicity-label">Black or African American</div>
        </Col>
        <Col span="5">
        <div class="ethnicity-count">
          <Icon type="md-arrow-up"/>
          {{group.white}}%
        </div>
        <div class="ethnicity-label">White</div>
        </Col>
        <Col span="6">
        <div class="ethnicity-count text-right">
          <Icon type="md-arrow-up"/>
          {{group.prefer_not_to_say}}%
        </div>
        <div class="ethnicity-label text-right">Not Said</div>
        </Col>
      </Row>
      <Poptip placement="bottom" width="300" class="food-popover" v-if="group.status == 'published'">
        <Button class="food-popover__btn"><div class="food-popover__btn__before"></div>Foods<div class="food-popover__btn__after"></div></Button>
        <div class="food-table" slot="content">
            <table>
                <thead>
                    <tr>
                      <th>Name</th>
                      <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="food in group.foods">
                        <td>{{food.name}}</td>
                        <td>
                          <div class="food_type food_type--veg" v-if="food['type'] == 'veg' || food['type'] == 'both'"></div>
                          <div class="food_type food_type--nonveg" v-if="food['type'] == 'non veg' || food['type'] == 'both'"></div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </Poptip>
    </div>
    <div class="card-body">
      <Row class="user-item" v-for="result in group.results" :key="result.id"
      v-drag-drop
      v-on:drag-start="handleDragStart"
      v-on:drag-over="handleDragOver"
      v-on:drag-enter="handleDragEnter"
      v-on:drag-leave="handleDragLeave"
      v-on:drag-end="handleDragEnd"
      v-on:drop="handleDrop"
      v-on:drag="handleDrag">
        <Col span="14">
          <div class="avatar">
            <div class="name-avatar" v-bind:style="result.survey_meta_data.avatar_gradient" size="small">{{result.name[0]}}</div>
          </div>
          <div class="user-info">
            <div class="username">{{result.name}}</div>
            <div class="phone">
              {{result.phone}}
              <a v-bind:href="'tel:' + result.phone" class="phone__icon">
                <Icon type="ios-call-outline"  />
              </a>
            </div>
          </div>
        </Col>
        <Col span="10" class="user-action" :class="{'is_locked':(group.isManagerAssigned || islocked), 'is_published': true}">
          <Button type="warning" class="make-manager-btn" size="small" v-if="!(group.isManagerAssigned || islocked)" @click="makeManager(group, result)">Make Manager</Button>
          <div v-else>
            <div v-if="(group.manager == result.id) || (group.manager.id == result.id)" class="role manager"><Icon type="md-ribbon" />Manager</div>
            <div v-else class="role attendee">Attendee</div>
          </div>
          <div class="email">{{result.email}}</div>
          <a :href="'select-food/group/' + group.id + '/user/' + result.id" target="_blank" v-if="group.status == 'published'">
            <Icon type="ios-menu" class="menu-btn" />
          </a>
        </Col>
      </Row>
    </div>
  </div>
</template>
<script>
import dragDrop from '@/directives/dragdrop'
export default {
  props: ['group', 'lockGroup', 'makeManager', 'islocked', 'undoManager', 'unlockPotluck', 'publishPotluck'],
  methods: {
    handleDragStart: function (e) {
      console.log('handleDragStart', e)
      this.loggedEvent = 'handleDragStart'
    },
    handleDragOver: function (e) {
      console.log('handleDragOver', e)
      this.loggedEvent = 'handleDragOver'
    },
    handleDragEnter: function (e) {
      console.log('handleDragEnter', e)
      this.loggedEvent = 'handleDragEnter'
    },
    handleDragLeave: function (e) {
      console.log('handleDragLeave', e)
      this.loggedEvent = 'handleDragLeave'
    },
    handleDragEnd: function (e) {
      console.log('handleDragEnd', e)
      this.loggedEvent = 'handleDragEnd'
    },
    handleDrop: function (e) {
      console.log('handleDrop', this.currentlyDragging, e.target)
      this.currentlyDragging = null
      this.loggedEvent = 'handleDrop'
    },
    handleImageDrop: function (e) {
      console.log('handleImageDrop', this.currentlyDragging, e.target)
      this.currentlyDragging = null
      this.loggedEvent = 'handleImageDrop'
    },
    handleDrag: function (e) {
      console.log('handleDrag', e)
      this.loggedEvent = 'handleDrag'
      if (!this.currentlyDragging) {
        this.currentlyDragging = e.srcElement
      }
    }
  }
}
</script>

<style lang="scss">
.card {
  overflow: auto;
  background-color: white;
  border-radius: 5px;
  border-radius: calc(0.375rem - 1px);
  box-shadow: 0px 0px 8px 1px #aba8a85c;
  margin: 9px;
  .card-header {
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid lightgray;
    position: relative;
    .food-popover {
      position: absolute;
      bottom: -16px;
      left: calc(50% - 33px);
      z-index: 10;
      .food-table {
        table {
          font-family: Consolas,Menlo,Courier,monospace;
          font-size: 12px;
          border-collapse: collapse;
          border-spacing: 0;
          empty-cells: show;
          border: 1px solid #e9e9e9;
          width: 100%;
          margin-bottom: 24px;
          th,td {
            border: 1px solid #e9e9e9;
            padding: 5px 10px;
            text-align: left;
          }
          th {
            background: #f7f7f7;
            white-space: nowrap;
            color: #5c6b77;
            font-weight: 600;
          }
        }
      }
      .ivu-poptip-rel {
        overflow: hidden;
        background: white;
      }
      .food-popover__btn {
        padding: 0px 16px;
        position: relative;
        border: 1px solid green;
        background: #01a2012e;
        color: green;
        border-radius: 1px;
        font-weight: bold;
        // border-radius: 0px;
        &__before, &__after {
          position: absolute;
          content: '';
          background: white;
          width: 10px;
          height: 10px;
          border-radius: 50%;
          top: 4px;
          z-index: 11;
          left: -6px;
          border: 1px solid green;
        }
        &__after {
          right: -6px;
          left: initial;
        }
      }
      .food_type {
        $side: 14px;
        $inside: 10px;
        height: $side;
        width: $side;
        position: relative;
        display: inline-block;
        margin-right: 6px;
        border: 1px solid green;
        box-sizing: initial;
        &:before {
          content: '';
          position: absolute;
          border-radius: 50%;
          height: $inside;
          width: $inside;
          top: ($side - $inside)/2;
          left: ($side - $inside)/2;
          background-color: green;
        }
        &--veg {
          border-color: green;
          &:before {
            background-color: green;
          }
        }
        &--nonveg {
          border-color: brown;
          &:before {
            background-color: brown;
          }
        }
      }
    }
    .potluck-date-info {
      color: #f34700;
      font-weight: 500;
      font-size: 13px;
      border-radius: 5px;
      text-align: center;
      margin-top: 3px;
      border: 1px dashed #f3470099;
    }
    .potluck-action {
      font-size: 18px;
      padding: 5px;
      margin-right: 5px;
      color: gray;
      cursor: pointer;
      &.potluck-action--unlock {
        color: $warning;
      }
    }
    .group-name {
      font-weight: 500;
      font-size: 14px;
      line-height: 30px;
      color: $content;
    }
    .total-users-count {
      font-weight: bold;
      color: black;
      font-size: 18px;
    }
    .ethnicity-container {
      margin-top: 12px;
      .ethnicity-count {
        color: #ED4C67;
        font-size: 13px;
        line-height: 12px;
        font-weight: 500;
        .ivu-icon {
          margin-left: -3px;
          margin-right: -2px;
        }
      }
      .ethnicity-label {
        color: #525f7f;
      }
    }

    .name-avatar {
      width: 30px;
      height: 30px;
      display: inline-block;
      border-radius: 50%;
      text-align: center;
      line-height: 30px;
      color: white;
    }
  }
  .card-body {
    .user-item {
      padding: 0.5rem 1.5rem;
      border-bottom: 1px solid lightgray;
      overflow: hidden;
      .avatar {
        display: inline-block;
        float: left;
        margin-right: 10px;
        .name-avatar {
          width: 25px;
          height: 25px;
          display: inline-block;
          border-radius: 50%;
          text-align: center;
          line-height: 25px;
          color: white;
        }
      }
      .user-info {
        display: inline-block;
        float: left;
        .username {
          color: $title;
          font-size: 0.8375rem;
          line-height: initial;
          font-weight: bold;
        }
        .phone {
          color: $title;
          font-size: 0.775rem;
          .phone__icon {
            font-size: 16px;
            margin-top: -4px;
            margin-left: 2px;
            cursor: pointer;
            color: inherit;
            // margin-right: 5px;
          }
        }
      }
      .user-action {
        text-align: right;
        position: relative;
        padding-top: 18px;
        .menu-btn {
          color: #ce8a35;
          font-size: 12px;
          font-weight: bold;
          padding-left: 3px;
          cursor: pointer;
        }
        .email {
          color: $title;
          display: inline-block;
          margin-top: 2px;
        }
        .make-manager-btn{
          display: none;
          margin-top: 0px;
          font-size: 10px;
          padding: 0px 5px;
          background: initial;
          color: #f90;
          line-height: 14px;
          vertical-align: top;
          position: absolute;
          top: 0px;
          right: 0px;
        }
        .role {
          font-weight: 500;
          color: white;
          width: 75px;
          float: right;
          border-radius: 2px;
          font-size: 13px;
          &.manager {
            color: $warning;
            position: absolute;
            top: 0px;
            right: 0px;
          }
          &.attendee {
            color: $success;
            position: absolute;
            top: 0px;
            right: 0px;
          }
        }
      }
      &:hover .user-action {
        .make-manager-btn{
          display: initial;
        }
        &.is_locked {
          .email {
            display: inline-block;
          }
        }
      }

    }
  }
}
</style>
