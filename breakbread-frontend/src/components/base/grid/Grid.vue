<template>
  <div>
    <div class="grid">
        <div class="grid-options-bar">
            <div class="grid-options-bar__title">{{title}}</div>
            <div class="grid-options-bar__pagination-info"
                >{{(currentPage - 1) * pageSize + 1}} - {{currentPage * pageSize > totalRecords ? totalRecords : currentPage * pageSize}} of {{totalRecords}}
            </div>
            <div class="grid-actions">
                <div class="grid-actions__item" v-on:click="gridPaginate(previousPage)">
                    <Icon class="grid-actions__item__icon" type="ios-arrow-back"/>
                </div>
                <div class="grid-actions__item" v-on:click="gridPaginate(nextPage)">
                    <Icon class="grid-actions__item__icon" type="ios-arrow-forward"/>
                </div>
                <div class="grid-actions__item">
                    <Icon class="grid-actions__item__icon" type="ios-expand"/>
                </div>
                <div class="grid-actions__item" @click="showUploadModal = true" v-if="options.can_upload">
                    <Icon class="grid-actions__item__icon" type="md-cloud-upload" />
                </div>
                <div class="grid-actions__item" @click="exportCSV" v-if="options.can_upload">
                    <Icon class="grid-actions__item__icon" type="ios-cloud-download-outline"/>
                </div>
                <div class="grid-actions__item" v-on:click="gridReset()">
                    <Icon class="grid-actions__item__icon" type="md-refresh"/>
                </div>
                <div class="grid-actions__item" v-on:click="gridAddRow()" v-if="options.can_add">
                    <Icon class="grid-actions__item__icon" type="md-add" />
                </div>

            </div>
        </div>
        <div class="grid-table">
            <div class="grid-table__header" v-if="show_header">
                <div class="grid-table__header__row">
                    <div class="th noselect"
                        v-for="(headerObj, gridHeaderIndex) in headers"
                        v-bind:key="gridHeaderIndex"
                        v-on:click="gridSort(headerObj.key)"
                        :class='{"sorted-asc": headerObj.key == sortKey, "sorted-des": `-${headerObj.key}` == sortKey}'
                        >
                        {{headerObj.title.toLocaleUpperCase()}}
                        <div class="sort-block">
                            <Icon class="sort-block__icon sort-block__icon--asc" type="md-arrow-dropup"/>
                            <Icon class="sort-block__icon sort-block__icon--des" type="md-arrow-dropdown"/>
                        </div>
                    </div>
                    <div class="th noselect th--spacer" v-if="show_spacer">
                        <Icon type="md-more" />
                    </div>
                </div>
            </div>
            <div class="grid-table__body">
                <div class="grid-table__body__row"
                    v-for="(newGridRow, newGridRowIndex) in newGridResults"
                    v-bind:key="newGridRowIndex"
                    >
                    <slot v-bind:newGridResults="newGridResults" v-bind:newGridRow="newGridRow" v-bind:newGridRowIndex="newGridRowIndex" v-bind:gridAdd="gridAdd" name="grid_data_new_td">
                    </slot>
                </div>
                <slot v-bind:gridResults="gridResults" v-bind:filterObj="filterObj"  name="grid_data_row">
                  <div class="grid-table__body__row"
                    v-for="(gridRow, gridRowIndex) in gridResults"
                    v-bind:key="gridRowIndex"
                    >
                    <div class="td"
                        v-for="(tdValue, filterKey, gridTdIndex) in  filterObj"
                        v-bind:key="gridTdIndex"
                        >{{gridRow[filterKey]}}</div>
                    <div class="td td--spacer" v-if="show_spacer"></div>
                  </div>
                </slot>

            </div>
        </div>
        <div class="grid-table" v-if="newGridResults.length == 0 &&  gridResults.length == 0 && gridLoading == false">
          <div class="grid-table__body__row" >
            <div class="td td--no-data-found">
              <slot name="grid_no-data">
                <Icon type="ios-albums-outline" class="td--no-data-found__icon"/> </br>
                No Data Found
              </slot>
            </div>
          </div>
        </div>
        <div class="grid-table" v-if="gridLoading == true">
          <div class="grid-table__body__row" >
            <div class="td td--loading">
              <slot name="grid_loading">
                <img class="td--loading__img" src="@/assets/images/bread-loading.svg" />
              </slot>
            </div>
          </div>
        </div>

    </div>
    <Modal v-model="showUploadModal" width="40%" class="uploads-modal">
        <p slot="header">
            <span>Import surveys by CSV file</span>
        </p>
        <div style="text-align:center" class="upload-widget-container" :class="{ 'upload-widget-disabled': !!csvFile }">
            <Upload
                type="drag"
                action="http://localhost:8000/api/potluck/"
                :before-upload="handleCSVUpload"
                :disabled="!!csvFile"
                accept=".csv">
                <div style="padding: 20px 0">
                    <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                    <p>Click or drag csv files here to upload</p>
                </div>
            </Upload>
            <div class="file-container">
                <div class="csv-file-name" v-if="!!csvFile">{{ csvFile.name }} <Icon type="ios-close-circle-outline" @click="csvFile = null"/></div>
            </div>

        </div>
        <div slot="footer">
            <Button size="large" @click="csvFile = null;showUploadModal=false">Cancel</Button>
            <Button type="primary" :disabled="!csvFile" size="large" :loading="showUploadModal_loading" @click="importCSV">Upload</Button>
        </div>
    </Modal>
  </div>
</template>
<script>
import { api } from '@/http'
export default {
  data () {
    var dataObj = {
      csvUrl: '',
      title: '',
      apiUrl: '',
      sortKey: '',
      queryObj: {},
      pageSize: 10,
      totalRecords: 0,
      nextPage: null,
      previousPage: null,
      currentPage: 1,
      showUploadModal: false,
      showUploadModal_loading: false,
      csvFile: undefined,
      gridResults: [],
      newGridResults: [],
      gridLoading: false,
      filterObj: {},
      show_header: true,
      show_spacer: false,
      options: {
        can_download: true,
        can_upload: true,
        can_add: false
      }
    }
    let options = { ...dataObj.options, ...this.config.options }
    return { ...dataObj, ...this.config, options }
  },
  methods: {
    gridAddRow () {
      this.newGridResults.push(this.headers.reduce((acc, header, index, val) => { acc[header['key']] = ''; return acc }, {}))
    },
    gridPropsReset () {
      this.queryObj = {}
      this.pageSize = 10
      this.totalRecords = 0
    },
    gridReset () {
      this.currentPage = 1
      this.gridPropsReset()
      this.gridLoad()
    },
    handleCSVUpload (file) {
      this.csvFile = file
      return false
    },
    importCSV () {
      let formData = new FormData()
      formData.append('file', this.csvFile)
      api
        .post(this.csvUrl, formData, { headers: { 'Content-Type': 'multipart/form-data' } }).then(response => {
          this.$Notice.success({
            title: 'Success',
            desc: response.message
          })
          this.gridLoad()
        }).catch(error => {
          this.$Notice.error({
            title: 'Error',
            desc: error
          })
        }).finally(() => {
          this.csvFile = null
          this.showUploadModal = false
        })
    },
    exportCSV () {
      api
        .get(this.csvUrl, { responseType: 'stream', headers: { 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'text/csv' } }).then(response => {
          var blob = new Blob([response], { type: 'text/csv' })
          var filename = this.title.split(' ').join('_')
          if (window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveBlob(blob, filename)
          } else {
            var elem = window.document.createElement('a')
            elem.href = window.URL.createObjectURL(blob)
            elem.download = filename
            document.body.appendChild(elem)
            elem.click()
            document.body.removeChild(elem)
          }
        }).catch(error => {
          this.$Notice.error({
            title: 'Error',
            desc: error
          })
        })
    },
    gridAdd (newGridRow, newGridRowIndex) {
      api
        .post(this.apiUrl, JSON.stringify(newGridRow)).then(response => {
          this.$Notice.success({
            title: 'Success',
            desc: 'Row Added Successfully'
          })
          this.newGridResults.splice(newGridRowIndex, 1)
          this.gridLoad()
        }).catch(error => {
          this.$Notice.error({
            title: 'Error',
            desc: error
          })
        })
    },
    gridLoad () {
      let params = {
        params: JSON.parse(JSON.stringify(this.queryObj))
      }
      let that = this
      this.gridLoading = true
      this.gridResults = []
      this.totalRecords = 0
      api
        .get(this.apiUrl, {
          ...params
        })
        .then(response => {
          this.gridResults = response.results
          this.totalRecords = +response.count
          this.nextPage = response.next
            ? +new URL(response.next).searchParams.get('page') || null
            : null
          this.previousPage = response.previous
            ? new URL(response.previous).searchParams.get('page') || 1
            : 1
        })
        .catch(error => {
          this.$Notice.error({
            title: 'Error',
            desc: error.message
          })
          this.handleReset('formValidate')
        })
        .finally(() => {
          this.gridLoading = false
        })
    },
    gridPaginate (page) {
      if (!!page && page != this.currentPage) {
        this.currentPage = page
        this.queryObj['page'] = page
        this.gridLoad()
      } else {
        delete this.queryObj['page']
      }
    },
    gridSort (value) {
      this.sortKey =
        this.sortKey == value
          ? '-' + value
          : this.sortKey == '-' + value
            ? value
            : value
      this.currentPage = 1
      this.queryObj['ordering'] = this.sortKey
      this.addFilterParams()
      this.gridPaginate()
      this.gridLoad()
    },
    addFilterParams () {
      let data = JSON.parse(JSON.stringify(this.filterObj))
      for (let [key, value] of Object.entries(data)) {
        value = value.trim()
        value
          ? (this.queryObj[key + '__icontains'] = value)
          : delete this.queryObj[key + '__icontains']
      }
    },
    gridFilter () {
      this.addFilterParams()
      this.gridPaginate()
      this.gridLoad()
    }
  },
  beforeMount () {
    this.gridLoad()
  },
  props: ['config']
}
</script>
<style lang="scss">
$spacer-width: 80px;
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
                    &--spacer {
                      width: $spacer-width;
                      padding-left: 0px !important;
                      padding-right: 0px !important;
                      text-align: center;
                    }
                    &.sorted-des {
                      color: $primary-dark;
                      .sort-block__icon--des {
                        display: none
                      }
                    }
                    &.sorted-asc {
                      color: $primary-dark;
                      .sort-block__icon--asc {
                        display: none
                      }
                    }
                    .sort-block {
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
                  &--spacer {
                    width: $spacer-width;
                    padding-left: 0px !important;
                    padding-right: 0px !important;
                    text-align: center;
                  }
                  &--loading {
                    text-align: center;
                    .td--loading__img {
                      max-width: 80px;
                    }
                  }
                  &--no-data-found {
                    &__icon {
                      font-size: 30px;
                      margin-bottom: 10px;
                    }
                    text-align: center;
                    color: gray !important;
                  }
                }
            }
        }
    }
}
</style>
