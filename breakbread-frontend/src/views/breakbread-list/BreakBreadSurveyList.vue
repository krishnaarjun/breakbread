<template>
  <div>
    <div class="content-inner">
      <div class="search-box">
        <Row>
          <Col span="24" class="search-header">Search Criteria</Col>
        </Row>
        <Form label-position="top">
          <Row :gutter="16" align="bottom" type="flex">
            <Col span="3" v-for="(filterValue, filterIndex) in surveyGrid.headers">
              <FormItem :label="filterValue.title">
                <Input v-model="surveyGrid.filterObj[filterValue.key]" clearable></Input>
              </FormItem>
            </Col>
            <Col span="3">
              <Button type="primary" v-on:click="$refs.dataGrid.gridFilter()">Search</Button>
            </Col>
          </Row>
        </Form>
      </div>
      <Grid :config="surveyGrid" ref="dataGrid">
        <template v-slot:grid_no-data>
            <Icon type="md-list-box" class="td--no-data-found__icon"/></br>
            No surveys found
        </template>
      </Grid>
    </div>
  </div>
</template>
<script>
import { api } from '@/http'
import Grid from '@/components/base/grid/Grid.vue'
export default {
  data () {
    return {
      surveyGrid: {
        queryObj: {},
        csvUrl: 'potluck/survey_csv/',
        title: 'Survey Registries',
        apiUrl: 'potluck/surveys/',
        headers: [
          {
            title: 'Name',
            key: 'name'
          },
          {
            title: 'Email',
            key: 'email'
          },
          {
            title: 'Phone',
            key: 'phone'
          },
          {
            title: 'Zipcode',
            key: 'zipcode'
          },
          {
            title: 'Ethnic Persuasion',
            key: 'ethnic_persuasion'
          },
          {
            title: 'Availability',
            key: 'availability'
          },

          {
            title: 'Hosting At',
            key: 'hosting_at'
          }
        ],
        filterObj: { name: '', email: '', phone: '', zipcode: '', ethnic_persuasion: '', availability: '', hosting_at: '' }
      }
    }
  },
  components: {
    Grid
  },
  methods: {
    updateFilterObj (filterObj, headers) {
      filterObj: headers.reduce((acc, header, index, val) => { acc[header['key']] = ''; return acc }, {})
    },
    beforeMount () {
      console.log('before mounted')
    }
  }
}
</script>

<style lang="scss">
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
