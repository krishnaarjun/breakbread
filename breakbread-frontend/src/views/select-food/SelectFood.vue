<template>
  <div class="food-select-container">
    <Row class="content-inner">
        <Col span="18" offset="3" class="select-food" :style="{ backgroundImage: `url(${require('@/assets/images/food-bg.jpg')})` }">
            <Col span="13" offset="11" class="select-food-menu" :style="{ backgroundImage: `url(${require('@/assets/images/menu-bg.jpg')})` }">
                <h1 class="banner">Break Bread Menu</h1>
				<div v-if="foodNotFound == false && potluckFoodsLoading == false">
					<div class="select-food-menu__helper" v-if="food_info.current_user_foods.length ==0">Select following food</div>
					<div class="select-food-menu__helper success" v-else>You have selected following food</div>
					<div class="food-menu-legend">
						<div class="food-menu-legend__pill" v-if="food_info.current_user_foods.length ==0">
							<div class="food-menu-legend__pill__icon food-menu-legend__pill__icon__available"></div>
							<div class="food-menu-legend__pill__name">Available</div>
						</div>
						<div class="food-menu-legend__pill" v-if="food_info.current_user_foods.length > 0">
							<div class="food-menu-legend__pill__icon food-menu-legend__pill__icon__selected"></div>
							<div class="food-menu-legend__pill__name">Selected</div>
						</div>
						<div class="food-menu-legend__pill">
							<div class="food-menu-legend__pill__icon food-menu-legend__pill__icon__unavailable"></div>
							<div class="food-menu-legend__pill__name">Unavailable</div>
						</div>
					</div>
					<div class="select-foods-list">
						<FoodItem v-for="food in food_info.available_foods" :key="food.id" :className="foodItemStatus(food.id)" :toggleFood="toggleFood" :food="food"></FoodItem>
					</div>

                    <Button type="primary" :loading="isSubmitting" size="large" class="select-food-menu__submit" :disabled="selected_foods.length == 0" @click="setFoodGroup()" v-if="food_info.current_user_foods.length == 0">
						<span v-if="!isSubmitting">SUBMIT</span>
        				<span v-else>SUBMITTING...</span>
					</Button>
                </div>
				<Col span="24" style="margin-top: 50px;text-align: center;" v-if="potluckFoodsLoading == true">
					<img src="@/assets/images/bread-loading.svg" style="max-width: 180px" />
				</Col>
                <div v-if="foodNotFound == true">
                    <img src="@/assets/images/food-list-not-found.png" style="max-width: 120px;margin-top: 80px"/>
                    <h1 style="margin-top: 10px; color: #a4815e; font-size: 22px; font-weight: inherit;">Menu is unavailable</h1>
                </div>
            </Col>
        </Col>
    </Row>
  </div>
</template>
<script>

import FoodItem from './FoodItem.vue'
import { api } from '@/http'
import { genGradient } from '@/services/utils'
export default {
  data () {
    return {
	  food_info: {
        available_foods: [],
        registered_foods: [],
        current_user_foods: []
	  },
	  selected_foods: [],
	  group_info: {},
	  user_info: {},
	  foodNotFound: false,
	  potluckFoodsLoading: true,
	  isSubmitting: false
    }
  },
  methods: {
    loadPotluckFoods () {
      this.potluckFoodsLoading = true
      api.get(`potluck/select_food/group/${this.$route.params.group_id}/user/${this.$route.params.user_id}/`, { hasPermission: true })
        .then(response => {
          this.group_info = response.group_info
          this.user_info = response.user_info
          this.food_info = response.food_info
          if (response.food_info.current_user_foods.length > 0) {
            let temp_food_list_1 = []; let temp_food_list_2 = []
            response.food_info.available_foods.forEach((foodObj, index) => {
              if (response.food_info.current_user_foods.includes(foodObj.id)) {
                temp_food_list_1.push(foodObj)
              } else {
                temp_food_list_2.push(foodObj)
              }
            })
            this.food_info.available_foods = [...temp_food_list_1, ...temp_food_list_2]
          } else if (response.food_info.registered_foods.length > 0) {
            let temp_food_list_1 = []; let temp_food_list_2 = []
            response.food_info.available_foods.forEach((foodObj, index) => {
              if (!response.food_info.registered_foods.includes(foodObj.id)) {
                temp_food_list_1.push(foodObj)
              } else {
                temp_food_list_2.push(foodObj)
              }
            })
            this.food_info.available_foods = [...temp_food_list_1, ...temp_food_list_2]
          }
          this.potluckFoodsLoading = false
        })
        .catch(error => {
          this.potluckFoodsLoading = false
          this.foodNotFound = true
          this.$Notice.error({
            title: 'Error',
            desc: error.message
		  })
        })
    },
    foodItemStatus (uuid) {
      if (this.food_info.current_user_foods.indexOf(uuid) != -1) {
        return 'selected'
      } else if (this.food_info.registered_foods.indexOf(uuid) != -1 || this.food_info.current_user_foods.length > 0) {
        return 'unavailable'
      } else if (this.selected_foods.indexOf(uuid) != -1) {
        return 'active'
      }
      return ''
    },
    toggleFood (uuid) {
      if (!['selected', 'unavailable'].includes(this.foodItemStatus(uuid))) {
        var index = this.selected_foods.indexOf(uuid)
        if (index === -1) {
          this.selected_foods.push(uuid)
        } else {
          this.selected_foods.splice(index, 1)
        }
      }
    },
    setFoodGroup () {
      this.isSubmitting = true
      api.post(`potluck/select_food/group/${this.$route.params.group_id}/user/${this.$route.params.user_id}/`, JSON.stringify({ selected_foods: this.selected_foods }), { hasPermission: true })
        .then(response => {
          this.$Notice.success({
            title: 'Success',
            desc: 'Food has been registered successfully'
          })
          this.isSubmitting = false
          this.loadPotluckFoods()
        })
        .catch(err => {
          this.isSubmitting = false
          this.$Notice.error({
            title: 'Error',
            desc: error.message
          })
        })
    }
  },
  computed: {},
  created () {
    this.loadPotluckFoods()
  },
  components: {
    FoodItem
  }
}
</script>
<style lang="scss" scoped>
.banner {
	position: relative;
    display: block;
    margin: 20px auto 0 auto;
    width: 60%;
    height: 50px;
    border: 1px solid #d28c36;
    text-align: center;
    color: white;
    background: #d28c36;
    border-radius: 4px;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.15) inset, 0 6px 10px rgba(0, 0, 0, 0.15);
	padding-top: 5px;
	&::before,&::after {
		content: '';
		position: absolute;
		z-index: -1;
		left: -66px;
		top: 24px;
		display: block;
		width: 40px;
		height: 0px;
		border: 25px solid #c88533;
		border-right: 20px solid #946224;
		border-bottom-color: #bf8031;
		border-left-color: transparent;
		transform: rotate(-5deg);
		box-sizing: initial;
	}

	&::after {
		left: auto;
		right: -70px;
		border-left: 20px solid #946224;
		border-right: 30px solid transparent;
		transform: rotate(5deg);
	}
}

.food-select-container {
    height: calc(100vh - 120px);
    .content-inner {
        height: 100%;
        padding: 25px 0;
        .select-food {
            height: 100%;
            background-repeat: no-repeat;
            background-size: cover;
            .select-food-menu {
                height: 100%;
                background-repeat: no-repeat;
                background-size: cover;
                text-align: center;
                position: relative;
				z-index: 1;
				.select-food-menu__helper {
					color: #003369;
					font-size: 26px;
					font-weight: 500;
					margin-top: 30px;
					&.success {
						color: #1a713f;
					}
				}
				.food-menu-legend {
					overflow: hidden;
					width: 300px;
					margin: 20px auto 0 auto;
					.food-menu-legend__pill {
						float: left;
						width: 33.33%;
						overflow: hidden;
						text-align: left;
						.food-menu-legend__pill__icon {
							height: 13px;
							width: 13px;
							border-radius: 50%;
							display: inline-block;
							margin: 3px 5px 0 0;
							line-height: 15px;
							vertical-align: top;
							&.food-menu-legend__pill__icon__available {
								background: #fdd3af
							}
							&.food-menu-legend__pill__icon__selected {
								background: #41bf6a;
							}
							&.food-menu-legend__pill__icon__unavailable {
								background: #AEAEAE;
							}

						}
						.food-menu-legend__pill__name {
							font-size: 12px;
							display: inline-block;
							color: black;
						}
					}
				}
				.select-foods-list{
					max-height: 330px;
					overflow: auto;
					width: 300px;
					text-align: center;
					margin: 5px auto 0 auto;
				}
                .select-food-menu__submit {
                    width: 200px;
					margin-top: 20px;
                    &[disabled] {
                        background-color: #a5cef8;
                        color: white;
                    }
                }
            }
        }
    }
}
</style>
