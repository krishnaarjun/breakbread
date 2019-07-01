<template>
    <div class="select-foods-item" name="select-foods-item" @click="toggleFood(food.id)" :class="className">
        <div class="select-icon"></div>
        <div class="select-name">
            <Tooltip :content="food.name" placement="top" :delay="1000">
                <div class="select-name__content">{{food.name}}</div>
            </Tooltip>
        </div>
        <div class="food-item-type">
            <div class="food_type food_type--veg" v-if="food['type'] == 'veg' || food['type'] == 'both'"></div>
            <div class="food_type food_type--nonveg" v-if="food['type'] == 'non veg' || food['type'] == 'both'"></div>
        </div>
    </div>
</template>
<script>
export default {
  props: ['className', 'food', 'toggleFood']
}
</script>
<style lang="scss" scoped>
.food-item-type {
    padding-top: 3px;
    display: inline-block;
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
        float: left;
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

.select-foods-item {
    border-radius: 5px;
    width: 100%;
    margin: 8px 0px;
    background: white;
    display: inline-block;
    padding: 12px 0;
    cursor: pointer;

    .select-icon {
        height: 20px;
        width: 20px;
        margin: 2px 20px 0 20px;
        float: left;
        background: #fbae6b8c;
        border-radius: 50%;
    }
    .select-name {
        width: calc(100% - 110px);
        float: left;
        text-align: left;
        font-size: 15px;
        font-weight: 500;
        color: #505a6e;
        .ivu-tooltip {
            width: 100%;
            .select-name__content {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
        }
    }
    &.active {
        background: #f3e3cd;
        .select-icon {
            background-color: #fbae6b;
        }
    }
    &.selected {
        background:#d3f7de;
        cursor: default;
        .select-icon {
            background-color: #41bf6a;
        }
    }
    &.unavailable {
        background: #ececec;
        cursor: default;
        .select-icon {
            background-color: #AEAEAE;
        }
    }
}
</style>
