<template>
  <div class="content-inner">
    <Button type="primary" size="large" @click="loadGroups" style="margin-right: 20px;">
        <Icon type="ios-shuffle" style="font-size: 22px; margin-right: 10px;"/> <span>Randomize</span>
    </Button>
    <Button size="large" @click="resetGroups">
      <Icon type="ios-refresh" style="font-size: 22px; margin-right: 10px;"/>Reset
    </Button>
    <Row class="code-row-bg" :gutter="50" style="margin-top: 10px;margin-bottom: 30px;">
      <Col span="8" v-for="group in groups" style="margin-top: 30px;" v-if="groups.length != 0 && groupsLoading == false">
        <PotluckTail :group="group" :lockGroup="lockGroup" :makeManager="makeManager" :undoManager="undoManager"></PotluckTail>
      </Col>
      <Col span="24" class="groups-not-found" v-if="groups.length == 0 && groupsLoading == false">
        <img src="@/assets/images/groups-unavailable.png" class="groups-not-found__image" />
        <div class="groups-not-found__description">No groups found</div>
        <!-- <router-link to="/groups" class="nav-link">
            <Button type="info" class="groups-not-found__btn">Go to groups</Button>
        </router-link> -->
      </Col>
      <Col span="24" style="margin-top: 50px;text-align: center;" v-if="groupsLoading == true">
        <img src="@/assets/images/bread-loading.svg" style="max-width: 180px" />
      </Col>
    </Row>
  </div>
</template>
<script>
import { genGradient } from '@/services/utils'
import { api } from '@/http'
import PotluckTail from '@/components/base/potluckTail/PotluckTail.vue'

export default {
  name: 'groups',
  data () {
    return {
      groups: [],
      groupLoading: false
    }
  },
  components: {
    PotluckTail
  },
  methods: {
    randomGradient () {
      return { background: genGradient() }
    },
    makeManager (group, manager) {
      group['isManagerAssigned'] = true
      group.manager = manager.id
    },
    undoManager (group) {
      group['isManagerAssigned'] = false
      delete group.manager
    },
    lockGroup (group) {
      var group = JSON.parse(JSON.stringify(group))
      var attendees = group.results.map(result => result.id)
      let data = { name: group.name, manager: group.manager, group_meta_data: group.group_meta_data, attendees, attendees_avatar_gradients: group.results.map(res => res.survey_meta_data.avatar_gradient) }
      api({
        method: 'post',
        url: 'potluck/potluckgroup/',
        data: JSON.stringify(data)
      })
        .then(response => {
          this.$Notice.success({
            title: 'Success',
            desc: 'Potluck has been locked'
          })
          this.loadGroups()
        })
        .catch(err => {
          console.log(err)
        })
    },
    resetGroups () {
      api
        .delete('potluck/potluckgroup/')
        .then(response => {
          this.loadGroups()
        })
        .catch(err => {
          console.log(err)
        })
    },
    loadGroups () {
      this.groupsLoading = true
      this.groups = []
      api
        .get('potluck/get_groups/')
        .then(response => {
          this.groupsLoading = false
          response.forEach(group => {
            let ethnic_persuasion = {
              black_or_african_american: 0,
              white: 0,
              prefer_not_to_say: 0
            }; let total_results = group.results.length
            group.results.forEach(result => {
              let ethnic_type = result['ethnic_persuasion']
              ethnic_persuasion[ethnic_type.replace(/\s/ig, '_')] += (1 / total_results) * 100
              result['survey_meta_data'] = { 'avatar_gradient': {} }
              result['survey_meta_data']['avatar_gradient'] = this.randomGradient()
            })
            group['white'] = ethnic_persuasion['white'].toFixed(1)
            group['black_or_african_american'] = ethnic_persuasion['black_or_african_american'].toFixed(1)
            group['prefer_not_to_say'] = ethnic_persuasion['prefer_not_to_say'].toFixed(1)
            group['group_meta_data'] = { 'avatar_gradient': {} }
            group['group_meta_data']['avatar_gradient'] = this.randomGradient()
            group['isManagerAssigned'] = false
          })
          this.groups = response
        })
        .catch(error => {
          this.groupsLoading = false
          console.log(error)
        })
    }
  },
  computed: {},
  created () {
    this.loadGroups()
  }
}
</script>
<style lang="scss">
.groups-not-found {
  text-align: center;
  margin-top: 50px;
  .groups-not-found__image {
    max-width: 180px;
  }
  .groups-not-found__description {
    font-size: 20px;
    margin-top: 15px;
  }
  .groups-not-found__btn {
    margin-top: 15px;
  }
}
</style>
