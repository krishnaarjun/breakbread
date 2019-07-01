<template>
  <div>
    <div class="content-inner">
      <div class="search-box">
        <Row>
          <Col span="24" class="search-header">Search Criteria</Col>
        </Row>
        <Row>
            <Col span="10">
                <Input v-model="foodListGrid.filterObj.name" v-on:on-search="$refs.foodListGrid.gridFilter()" search enter-button placeholder="Enter food name" />
            </Col>
        </Row>
      </div>
      <!-- <div style="margin-bottom: 20px">
          <Row>
              <Col span="10">
                <Input v-model="foodListGrid.filterObj.name" v-on:on-search="$refs.foodListGrid.gridFilter()" search enter-button placeholder="Enter food name" />
              </Col>
          </Row>
      </div> -->
      <Grid :config="foodListGrid" ref="foodListGrid">
        <template v-slot:grid_data_new_td="newRowGridData">
            <div class="td">
                <Input v-model="newRowGridData.name" placeholder="" />
            </div>
            <div class="td">
                <Select v-model="newRowGridData.type">
                    <Option  value="veg" key="veg">Veg</Option>
                    <Option  value="non veg" key="non veg">Non Veg</Option>
                    <Option  value="both" key="both">Both</Option>
                </Select>
            </div>
            <div class="td td--spacer" style="padding-top: 0;padding-bottom: 0;font-size: 22px">
                <Icon type="ios-add-circle-outline" style="color: green;margin-right: 5px;cursor: pointer" @click="onRowAdd(newRowGridData)"/>
                <Icon type="ios-trash-outline" style="color: red;cursor: pointer" @click="onRowDelete(newRowGridData)"/>
            </div>
        </template>
        <template v-slot:grid_no-data>
            <Icon type="md-restaurant" class="td--no-data-found__icon"/></br>
            No foods found
        </template>
        <template v-slot:grid_data_row="dataProps">
            <div class="grid-table__body__row" v-for="(gridRow, gridRowIndex) in dataProps.gridResults" v-bind:key="gridRowIndex">
                <div class="td" style="padding-top: 10px;padding-bottom: 10px;">
                    <div style="height: 30px;width: 30px; border-radius: 10px;display: inline-block;color: white;text-align: center;padding-top: 3px;font-weight: 500;margin-right: 6px;" v-bind:style="gridRow.meta_data.avatar_gradient">{{gridRow.name[0].toUpperCase()}}</div>
                    {{gridRow['name']}} <br>
                </div>
                <div class="td" style="padding-top: 10px;padding-bottom: 10px;">
                    <div class="food_type food_type--veg" v-if="gridRow['type'] == 'veg' || gridRow['type'] == 'both'"></div>
                    <div class="food_type food_type--nonveg" v-if="gridRow['type'] == 'non veg' || gridRow['type'] == 'both'"></div>
                </div>
                <div class="td td--spacer" style="padding-top: 10px;padding-bottom: 10px;"></div>
            </div>
        </template>
      </Grid>
    </div>
  </div>
</template>
<script>
import { genGradient } from '@/services/utils'
import { api } from '@/http'
import Grid from '@/components/base/grid/Grid.vue'
export default {
  data () {
    return {
      foodListGrid: {
        queryObj: {},
        csvUrl: 'potluck/foods/',
        title: 'Available Foods',
        apiUrl: 'potluck/foods/',
        headers: [
          {
            title: 'Name',
            key: 'name'
          },
          {
            title: 'Type',
            key: 'type'
          }
        ],
        filterObj: { name: '', type: '' },
        show_spacer: true,
        options: {
          can_download: false,
          can_upload: false,
          can_add: true
        }
      }
    }
  },
  components: {
    Grid
  },
  methods: {
    randomGradient () {
      return { background: genGradient() }
    },
    updateFilterObj (filterObj, headers) {
      filterObj: headers.reduce((acc, header, index, val) => { acc[header['key']] = ''; return acc }, {})
    },
    onRowAdd (props) {
      props.gridAdd({ name: props.name, type: props.type, meta_data: { avatar_gradient: this.randomGradient() } }, props.newGridRowIndex)
    },
    onRowDelete (props) {
      props.newGridResults.splice(props.newGridRowIndex, 1)
    },
    beforeMount () {
      console.log('before mounted')
    }
  }
}
</script>

<style lang="scss" scoped>
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
.search-box {
  background: white;
  border: 1px solid #edf1f6;
  border-radius: 2px;
  box-shadow: 0px 0px 1px #edf1f6;
  padding: 15px;
  margin-bottom: $inner-spacer;
  .search-header {
    font-size: 22px;
    font-weight: bold;
    margin: 0 0 10px 0;
  }
  .ivu-form-item {
    margin-bottom: 0px;
  }
}
.grid {
    background: white;
    .grid-options-bar {
        width: 100%;
        padding: 15px 20px;
        border: 1px solid $border-color;
        overflow: hidden;
        &__title {
            font-size: 18px;
            padding: 0px 20px 0 0;
            border-right: 1px solid $border-color;
            display: inline-block;
        }
        &__pagination-info {
            display: inline-block;
            padding-left: 20px;
            font-size: 14px;
            font-weight: bold;
            color: $light-color;
        }
        .grid-actions {
            float: right;
            &__item {
                display: inline-block;
                position: relative;
                z-index: 1;
                &:hover {
                    &:before {
                        content: "";
                        height: 30px;
                        width: 30px;
                        background: $border-color;
                        left: 0px;
                        border-radius: 50%;
                        top: -4px;
                        position: absolute;
                        z-index: -1;
                    }
                }
                &__icon {
                    color: $light-color;
                    font-weight: bold;
                    font-size: 18px;
                    padding: 0px 6px;
                    cursor: pointer;
                }
            }
        }

    }
    .grid-table {
        display: table;
        width: 100%;
        &__header {
            display: table-header-group;
            &__row {
                display: table-row;
                border: 1px solid $border-color;
                .th {
                    display: table-cell;
                    font-size: 13px;
                    padding: 10px 20px;
                    color: #8a8a8a;
                    border-bottom: 1px solid $border-color;
                    cursor: pointer;
                    position: relative;
                    .sort-block {
                        $sort-block: &;
                        display: inline-block;
                        margin-top: 10px;
                        position: absolute;
                        right: 15px;
                        &__icon {
                            position: absolute;
                            font-size: 16px;
                            right: 5px;
                            display: initial;
                            &.ivu-icon-md-arrow-dropup {
                                bottom: -4px;
                            }
                            &.ivu-icon-md-arrow-dropdown {
                                top: -4px;
                            }
                        }
                        &--asc {
                            .sort-block__icon {
                                &.ivu-icon-md-arrow-dropup {
                                    display: none;
                                }
                            }
                        }
                        &--desc {
                            .sort-block__icon {
                                &.ivu-icon-md-arrow-dropdown {
                                    display: none;
                                }
                            }
                        }
                    }
                }
            }
        }
        &__body {
            display: table-row-group;
            width: 100%;
            border: 1px solid $border-color;
            &__row {
                display: table-row;
                border: 1px solid $border-color;
                .td {
                    font-size: 16px;
                    border-bottom: 1px solid $border-color;
                    color: black;
                    display: table-cell;
                    padding: 20px;
                }
            }
        }
    }
}
.upload-widget-container {
  &.upload-widget-disabled {
    .ivu-upload {
      cursor: disabled;
      .ivu-upload-drag:hover{
        border: 1px dashed #dcdee2;
      }
      & * {
        color: gray !important;
      }

    }
  }
  .file-container {
    height: 30px;
    .csv-file-name {
      font-size: 18px;
      overflow: hidden;
      padding: 0px 10%;
      height: inherit;
      color: $primary;
      &:hover {
        background-color: rgba(208, 205, 205, 0.47843137254901963);
        .ivu-icon {
          visibility: initial;
        }
      }
      margin: auto;
      .ivu-icon {
        float: right;
        margin-top: 7px;
        cursor: pointer;
        visibility: hidden;
      }
    }
  }
}

</style>
