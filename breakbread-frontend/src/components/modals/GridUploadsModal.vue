<template>
    <Modal v-model="showUploadModal" width="40%">
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
</template>

<style lang="scss">
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
