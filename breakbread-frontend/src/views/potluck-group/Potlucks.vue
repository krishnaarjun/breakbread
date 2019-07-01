<template>
  <div class="content-inner">
    <Tabs :animated="false" type="card" v-model="tab">
      <TabPane label="Locked" icon="md-lock"  name="locked">
        <Row class="code-row-bg" :gutter="50">
          <div v-if="lockedPotlucks.length > 0 && potlucksLoading == false">
            <Col span="8" v-for="group in lockedPotlucks" style="margin-top: 30px;"  :key="group.id">
                <PotluckTail  :group="group" islocked="true" :unlockPotluck="unlockPotluck" :publishPotluck="publishPotluck"></PotluckTail>
            </Col>
          </div>
          <Col span="24" class="potlucks-not-found" v-if="lockedPotlucks.length == 0 && potlucksLoading == false">
            <img src="@/assets/images/locked-potlucks-unavailable.png" class="potlucks-not-found__image" />
            <div class="potlucks-not-found__description">No potluck groups were locked</div>
            <router-link to="/groups" class="nav-link">
                <Button type="info" class="potlucks-not-found__btn">Go to groups</Button>
            </router-link>
          </Col>
          <Col span="24" style="margin-top: 50px;text-align: center;" v-if="potlucksLoading == true">
            <img src="@/assets/images/bread-loading.svg" style="max-width: 180px" />
          </Col>
        </Row>
      </TabPane>
      <TabPane label="Published" icon="md-checkbox-outline" name="published">
        <Row class="code-row-bg" :gutter="50" >
          <div v-if="publishedPotlucks.length > 0 && potlucksLoading == false">
          <Col span="8" v-for="group in publishedPotlucks" style="margin-top: 30px;" :key="group.id">
              <PotluckTail :group="group" islocked="true"></PotluckTail>
          </Col>
          </div>
          <Col span="24" class="potlucks-not-found" v-if="publishedPotlucks.length == 0 && potlucksLoading == false">
            <img src="@/assets/images/published-potlucks-unavailable.png" class="potlucks-not-found__image"/>
            <div class="potlucks-not-found__description">Seems like you did't publish any potluck yet.</div>
            <Button type="info" class="potlucks-not-found__btn" @click="tab = 'locked'">Go to locked potlucks</Button>
          </Col>
          <Col span="24" style="margin-top: 50px;text-align: center;" v-if="potlucksLoading == true">
            <img src="@/assets/images/bread-loading.svg" style="max-width: 180px" />
          </Col>
        </Row>
      </TabPane>
    </Tabs>
    <Modal v-model="showPotluckLockModal" width="40%">
        <p slot="header">
            <span>Publish Potluck</span>
        </p>
        <div style="text-align:center">
          <Form ref="editablePotluck" :model="editablePotluck" :rules="publishPotluckValidate" :label-width="150">
              <FormItem label="Group Name" prop="name">
                  <Input v-model="editablePotluck.name"></Input>
              </FormItem>
              <FormItem label="Select Foods" prop="foods">
                  <div class="auto-complete" @click="showFoodList = true" v-click-outside="onHideAutoComplete">
                    <Input type="text" v-model="food" class="auto-complete-input" @input="filterFood()"/></Input>
                    <div class="auto-complete-list" v-if="showFoodList">
                      <div v-if="filterdFoods.length > 0">
                        <div class="auto-complete-item food-item noselect food-item--random-field" @click.self="randomizeFood">
                          <Checkbox :value="isFoodRandomized" @on-change.self="randomizeFood">
                            <span class="mrl-5">Randomized Select</span>
                          </Checkbox>
                        </div>
                        <div  :key="food.id" v-for="food in filterdFoods" @click="addOrRemove(editablePotluck.foods, food.id)" class="auto-complete-item food-item noselect">
                          <Checkbox :value="editablePotluck.foods.includes(food.id)">
                          </Checkbox>
                          <span>{{food.name}}</span>
                          <div class="food-item-type">
                            <div class="food_type food_type--veg" v-if="food['type'] == 'veg' || food['type'] == 'both'"></div>
                            <div class="food_type food_type--nonveg" v-if="food['type'] == 'non veg' || food['type'] == 'both'"></div>
                          </div>
                        </div>
                      </div>
                      <div v-else class="text-center">
                          No food items found
                      </div>
                    </div>
                  </div>
                  <div class="food-pill-liner">
                    <div v-for="food in foods" :key="food.id">
                      <div class="food-pill"  v-if="editablePotluck.foods.includes(food.id)">{{food.name}}
                        <Icon type="ios-close-circle" class="food-pill-icon" @click="addOrRemove(editablePotluck.foods, food.id)"/>
                      </div>
                    </div>
                  </div>
              </FormItem>
              <FormItem label="Hosting On" style="text-align: left;"  prop="hosting_on">
                <DatePicker type="date" placeholder="Select date" v-model="editablePotluck.hosting_on" :start-date="new Date()" :options="dateOptions"></DatePicker>
                <!-- -
                <TimePicker type="time" placeholder="Select time" v-model="editablePotluck.hosting_on"></TimePicker> -->
              </FormItem>
          </Form>
        </div>
        <div slot="footer">
            <Button size="large" @click="onClosePublishPotluck">Cancel</Button>
            <Button type="primary" size="large" @click="onPublishPotluck">Publish</Button>
        </div>
    </Modal>
  </div>
</template>
<script>
import _ from 'lodash'
import PotluckTail from '@/components/base/potluckTail/PotluckTail.vue'
import clickOutside from '@/directives/clickoutside'
import { genGradient } from '@/services/utils'
import { api } from '@/http'

export default {
  data () {
    const validateFoods = (rule, value, callback) => {
      if (value.length <= 0) {
        callback(new Error('Select 5 foods'))
      } else {
        // if(value.length < 5) {
        //   callback(new Error("Foods cannot be less then 5"));
        // }
        callback()
      }
    }
    const validateDate = (rule, value, callback) => {
      if (!value) {
        callback(new Error('Hosting On cannot be empty'))
      } else {
        callback()
      }
    }
    return {
      lockedPotlucks: [],
      publishedPotlucks: [],
      potlucksLoading: false,
      showPotluckLockModal: false,
      isFoodRandomized: false,
      tab: 'locked',
      food: null,
      editablePotluck: {
        name: null,
        hosting_on: null,
        foods: [],
        id: null
      },
      food: '',
      showFoodList: false,
      foods: [],
      filterdFoods: [],
      publishPotluckValidate: {
        name: [
          { required: true, message: 'Group Name cannot be empty', trigger: 'blur' }
        ],
        foods: [
          { required: true, type: 'array', validator: validateFoods, trigger: 'change' }
        ],
        hosting_on: [
          { required: true, validator: validateDate, trigger: 'change' }
        ]
      },
      dateOptions: {
        disabledDate (date) {
          return date && date.valueOf() < Date.now() - 86400000
        }
      }
    }
  },
  components: {
    PotluckTail
  },

  methods: {
    onHideAutoComplete (event) {
      this.showFoodList = false
    },
    addOrRemove (array, value) {
      var index = array.indexOf(value)
      if (index === -1) {
        array.push(value)
      } else {
        array.splice(index, 1)
      }
      this.isFoodRandomized = false
      this.$refs.editablePotluck.$children[1].form.validate()
    },
    initEditablePotluck () {
      this.editablePotluck = { name: null, hosting_on: null, foods: [], id: null }
    },
    filterFood () {
      this.isFoodRandomized = false
      this.filterdFoods = this.foods.filter((fitem) => fitem.name.toLocaleLowerCase().startsWith(this.food.toLocaleLowerCase()))
    },
    randomizeFood () {
      if (!this.isFoodRandomized) {
        this.editablePotluck.foods = _.sampleSize(this.filterdFoods, _.random(5, 10)).map(foodobj => foodobj.id)
      }
      this.isFoodRandomized = !this.isFoodRandomized
      this.showFoodList = false
    },
    loadFoods () {
      api
        .get('potluck/foods/')
        .then(response => {
          this.foods = response.results
          this.filterdFoods = [...response.results]
        })
        .catch(err => {
          console.log(err)
        })
    },
    loadPotlucks () {
      this.potlucksLoading = true
      api
        .get('potluck/potluckgroup/')
        .then(response => {
          let data = response.results
          this.lockedPotlucks = []
          this.publishedPotlucks = []
          this.potlucksLoading = false
          data.forEach(potluck => {
            let ethnic_persuasion = {
              black_or_african_american: 0,
              white: 0,
              prefer_not_to_say: 0
            }; let total_results = potluck.attendees.length
            potluck.attendees.forEach(result => {
              let ethnic_type = result['ethnic_persuasion']
              ethnic_persuasion[ethnic_type.replace(/\s/ig, '_')] += (1 / total_results) * 100
            })
            potluck.results = potluck.attendees
            potluck['white'] = ethnic_persuasion['white'].toFixed(1)
            potluck['black_or_african_american'] = ethnic_persuasion['black_or_african_american'].toFixed(1)
            potluck['prefer_not_to_say'] = ethnic_persuasion['prefer_not_to_say'].toFixed(1)
            if (potluck.status === 'locked') {
              this.lockedPotlucks.push(potluck)
            } else if (potluck.status == 'published') {
              this.publishedPotlucks.push(potluck)
            }
          })
          // console.log(JSON.parse(JSON.stringify(this.potlucks)));
        })
        .catch(err => {
          this.potlucksLoading = false
          console.log(err)
        })
    },
    unlockPotluck (id) {
      api
        .delete(`potluck/potluckgroup/${id}`)
        .then(response => {
          this.$Notice.success({
            title: 'Success',
            desc: response.message
          })
          this.loadPotlucks()
        })
    },
    publishPotluck (potluck) {
      this.showPotluckLockModal = true
      this.isFoodRandomized = false
      this.editablePotluck = { name: potluck.name, foods: [...potluck.foods], hosting_on: potluck.hosting_on, id: potluck.id }
    },
    onPublishPotluck () {
      let id = this.editablePotluck.id
      this.editablePotluck.status = 'published'
      this.editablePotluck.hosting_on = this.editablePotluck.hosting_on.toISOString()
      let editablePotluck = JSON.stringify(this.editablePotluck)
      this.$refs.editablePotluck.validate((valid) => {
        if (valid) {
          api
            .patch(`potluck/potluckgroup/${id}`, editablePotluck)
            .then(response => {
              this.$Notice.success({
                title: 'Success',
                desc: response.message
              })
              this.loadPotlucks()
            })
            .catch(err => {
              this.$Notice.error({
                title: err.status,
                desc: err.message
              })
              this.loadPotlucks()
            })
            .finally(() => {
              this.showPotluckLockModal = false
              this.initEditablePotluck()
              this.$refs.editablePotluck.resetFields()
            })
        } else {
          this.$Notice.error({
            title: 'Failed to Publish',
            desc: 'Fill all the required fields'
          })
        }
      })
    },
    onClosePublishPotluck () {
      this.showPotluckLockModal = false
      this.initEditablePotluck()
      this.$refs.editablePotluck.resetFields()
    }
  },
  computed: {},
  created () {
    this.loadPotlucks()
    this.loadFoods()
  }
}
</script>
<style lang="scss">
.potlucks-not-found {
  text-align: center;
  margin-top: 50px;
  .potlucks-not-found__image {
    max-width: 180px;
  }
  .potlucks-not-found__description {
    font-size: 20px;
    margin-top: 15px;
  }
  .potlucks-not-found__btn {
    margin-top: 15px;
  }
}
.food_type {
    $side: 12px;
    $inside: 8px;
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
.food-pill-liner {
  margin-top: 10px;
  border: 1px solid #dcdee2;
  border-radius: 4px;
  overflow: auto;
  min-height: 50px;
  padding: 10px;
  .food-pill {
    float: left;
    background: #c3fdc342;
    border: 1px solid #66ab66;
    color: green;
    padding: 1px 2px 2px 5px;
    font-size: 11px;
    margin: 5px;
    display: inline-block;
    line-height: initial;
    border-radius: 10px;

    .food-pill-icon {
      color: #368636e3;
      margin-left: 5px;
      cursor: pointer;
      font-size: 14px;
      vertical-align: top;
    }
  }
}
.auto-complete {
  position: relative;
  .auto-complete-input {

  }
  .auto-complete-list {
    box-shadow: 0 1px 6px rgba(0,0,0,.2);
    overflow: auto;
    margin: 5px 0;
    padding: 5px 0;
    background-color: #fff;
    box-sizing: border-box;
    border-radius: 4px;
    z-index: 900;
    position: absolute;
    transform-origin: center top;
    top: 30px;
    min-height: 75px;
    max-height: 150px;
    width: 100%;
    .auto-complete-item {
      overflow: auto;
      padding: 0px 10px;
      cursor: pointer;
      &.food-item {
        text-align: left;
        &:hover{
          background: #e8e8e8;
        }
        &.food-item--random-field {
          color: #2b85e4;
          font-weight: 500;
          border-bottom: 1px solid #d3d3d359;
        }
        .food-item-type {
          float: right;
          line-height: initial;
          padding-top: 10px;
        }

      }
    }
  }
}
.ivu-tabs-nav {
  .ivu-icon {
    font-size: 18px;
    line-height: 21px;
    vertical-align: top;
  }
}
</style>
