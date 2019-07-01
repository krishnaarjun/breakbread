<template>
  <div>
    <div class="survey-form">
      <h1 class="jumbo-text text-center">BREAK BREAD WINSTON-SALEM</h1>
      <p class="description">
        You are invited to join Love Out Loud, the New Canaan Society, and the Skunkworks Committee on Racial Reconciliation in following Jesus' model of breaking bread together in private homes with people different than ourselves. Break Bread Winston-Salem is an evening of private dinners across our city the goal of which is to gather in the name of Jesus and grow relationally as a city by meeting new people, working on challenging cultural blind spots, and sharing our hopes and burdens. We desire to foster relationships across racial, geographical, socio-economic and denominational lines in our city.
        Each dinner will have two couples or individuals as co-hosts and will engage 10-12 people per home. Dinner menu and location will be decided by the co-hosts who will also serve as discussion facilitators through the meal, with suggested readings distributed ahead of time.
      </p>
      <Form
        class="form"
        ref="formValidate"
        :model="formValidate"
        :rules="ruleValidate"
        v-if="isFormSubmitted == false"
      >
        <h1 class="form-header">Registration Form</h1>
        <div class="form-description">
          All the
          <span class="error">*</span>fields are mandatory
        </div>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="11">
            <label>
              <span class="error">*</span>Name:
            </label>
            <FormItem prop="name">
              <Input size="large" placeholder="Enter" v-model="formValidate.name"></Input>
            </FormItem>
          </Col>
          <Col span="11">
            <label>
              <span class="error">*</span>Email:
            </label>
            <FormItem prop="email">
              <Input size="large" placeholder="your@email.com" v-model="formValidate.email"></Input>
            </FormItem>
          </Col>
        </Row>
        <br>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="11">
            <label>
              <span class="error">*</span>Phone:
            </label>
            <FormItem prop="phone">
              <Input size="large" placeholder="Enter" v-model.number="formValidate.phone"></Input>
            </FormItem>
            <!-- <Row type="flex" justify="space-between" class="code-row-bg">
            <Col span="7">
              <Input size="large" placeholder="Enter"/>
            </Col>
            <Col span="7">
              <Input size="large" placeholder="Enter"/>
            </Col>
            <Col span="7">
              <Input size="large" placeholder="Enter"/>
            </Col>
            </Row>-->
          </Col>
          <Col span="11">
            <label>
              <span class="error">*</span>Zip Code:
            </label>
            <FormItem prop="zipcode">
              <Input size="large" placeholder="Enter Zip Code" v-model="formValidate.zipcode"></Input>
            </FormItem>
          </Col>
        </Row>
        <br>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="11">
            <label>
              <span class="error">*</span>Ethnic persuasion:
            </label>
            <FormItem prop="ethnic_persuasion">
              <Select style="width:100%" v-model="formValidate.ethnic_persuasion">
                <Option value="black or african american">Black or African American</Option>
                <Option value="white">white</Option>
                <Option value="prefer not to say">prefer not to say</Option>
              </Select>
            </FormItem>
          </Col>
          <Col span="11">
            <label>
              <span class="error">*</span>Availability:
            </label>
            <FormItem prop="available_at">
              <CheckboxGroup v-model="formValidate.available_at">
                <Checkbox label="Tuesday"></Checkbox>
                <Checkbox label="Thursday"></Checkbox>
              </CheckboxGroup>
            </FormItem>
          </Col>
        </Row>
        <br>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="11">
            <label>
              <span class="error">*</span> 1-2 involved:
            </label>
            <FormItem prop="involved">
              <Input
                size="large"
                placeholder="Enter the count of people attending"
                type="textarea"
                v-model="formValidate.involved"
              ></Input>
            </FormItem>
          </Col>
          <Col span="11">
            <label>Church affiliation:</label>
            <FormItem prop="church_affiliation">
              <Input
                size="large"
                placeholder="Enter affiliation info"
                type="textarea"
                v-model="formValidate.church_affiliation"
              ></Input>
            </FormItem>
          </Col>
        </Row>
        <br>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="11">
            <label>
              <span class="error">*</span> Will you host in your home / park / church fellowship hall?
            </label>
            <br>
            <FormItem prop="hosting_at">
              <RadioGroup v-model="formValidate.hosting_at">
                <Radio label="home">Home</Radio>
                <Radio label="church">Church</Radio>
              </RadioGroup>
            </FormItem>
          </Col>
          <Col span="11">
            <label>Dietary restrictions or allergies</label>
            <br>
            <FormItem prop="dietary_restrictions_or_allergies">
              <Input
                size="large"
                placeholder="Enter if any dietary priorities or allergic foods"
                type="textarea"
                v-model="formValidate.dietary_restrictions_or_allergies"
              ></Input>
            </FormItem>
          </Col>
        </Row>
        <br>
        <Row type="flex" justify="space-between" class="code-row-bg">
          <Col span="24">
            <label>
              <span class="error">*</span>How Did you hear about Break Bread?
            </label>
            <br>
            <FormItem prop="heard_from">
              <CheckboxGroup v-model="formValidate.heard_from">
                <div v-for="(value,key) in heard_from_options" :key="value.id" v-if="value['type']=='default'">
                  <Checkbox :label="value.medium">{{value.medium}}</Checkbox>
                  <br>
                </div>
              </CheckboxGroup>
            </FormItem>
            <FormItem prop="other_medium" v-if="formValidate.heard_from === 'other'">
              <Input
                size="large"
                placeholder="Enter the source"
                type="textarea"
                v-model="formValidate.other_medium"
              ></Input>
              <br>
            </FormItem>

            <label>Comments or Questions</label>
            <br>
            <FormItem prop="comments_and_queries">
              <Input
                size="large"
                placeholder="Enter any comments or queries"
                type="textarea"
                v-model="formValidate.comments_and_queries"
              ></Input>
            </FormItem>
          </Col>
        </Row>
        <Button type="info" @click="handleSubmit('formValidate')">SUBMIT</Button>
        <Button @click="handleReset('formValidate')" style="margin-left: 8px">Reset</Button>
      </Form>
      <Card class="success-card" v-else>
        <div style="text-align:center">
          <Icon type="md-checkmark-circle-outline"/>
          <h3>You have been successfully registered</h3>
        </div>
      </Card>
    </div>

    <Modal
      width="50%"
      v-model="openIsAgreeModal"
      title="Agreement"
      @on-ok="agree(true)"
      on-cancel="agree(false)"
      ok-text="Agree"
      cancel-text="Disagree"
      class-name="agree-modal"
    >
      <div
        class="heading"
      >Agreement that personal information can be used by New Canaan Society or Love out Loud to facilitate the Break Bread engagement – including representation that your email and personal information will never be sold or provided to a 3rd party - You will always have an opportunity to opt out . . . and other legal stuff . . .</div>
      <p class="helper">Agreement that you are notionally committing to</p>
      <ul class="content">
        <li>6 dinners that rotate to different locations</li>
        <li>participating in potluck style with your participation in rotating meal items (takeout is always okay too)</li>
        <li>willingness to listen and engage with others that will have different backgrounds in their upbringing, community, and faith journey</li>
      </ul>
    </Modal>
  </div>
</template>

<script>
// grecaptcha.ready(function() {
//   grecaptcha
//     .execute("6LdayKAUAAAAACu8yDZ9BAJCAL23h5vAnhXcMub-", {
//       action: "homepage"
//     })
//     .then(function(token) {
//       console.log(token);
//     });
// });
import { api } from '@/http'
export default {
  data () {
    const validateEmail = (rule, value, callback) => {
      let emailPattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if (value === '') {
        callback(new Error('Enter you email'))
      } else {
        if (!emailPattern.test(String(value).toLowerCase())) {
          callback(new Error('Please enter valid email'))
        }
        callback()
      }
    }
    const validatePhoneNumber = (rule, value, callback) => {
      let phoneNumberPattern = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/
      if (value === '') {
        callback(new Error('Enter your number'))
      } else {
        if (!phoneNumberPattern.test(value)) {
          callback(new Error('Enter valid number'))
        }
        callback()
      }
    }
    const validateZipCode = (rule, value, callback) => {
      let isValidZip = /(^\d{5}$)|(^\d{5}-\d{4}$)/.test(value)
      if (value === '') {
        callback(new Error('Enter zip code'))
      } else {
        if (!isValidZip) {
          callback(new Error('Enter valid zip code'))
        }
        callback()
      }
    }
    const otherMediumValidate = (rule, value, callback) => {
      if (this.formValidate.heard_from === 'other' && value == '') {
        callback(new Error('Please enter the other source'))
      }
      callback()
    }
    const heardFromValidator = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('Please choose the source you heard from '))
      }
      callback()
    }
    const availableAtValidator = (rule, value, callback) => {
      if (value.length === 0) {
        callback(new Error('Please check the available time'))
      } else {
        this.formValidate.availability =
          value.length == 0
            ? value[0].toLocaleLowerCase()
            : 'tuesday and thursday'
      }
      callback()
    }
    return {
      openIsAgreeModal: false,
      isFormSubmitted: false,
      heard_from_options: {},
      formValidate: {
        name: '',
        email: '',
        phone: '',
        zipcode: '',
        ethnic_persuasion: '',
        involved: '',
        church_affiliation: '',
        available_at: [],
        availability: '',
        hosting_at: '',
        dietary_restrictions_or_allergies: '',
        heard_from: [],
        other: '',
        comments_and_queries: '',
        other_medium: '',
        is_agreed: false,
        comments_and_queries: ''
      },
      ruleValidate: {
        name: [
          {
            required: true,
            message: 'The name cannot be empty',
            trigger: 'blur'
          }
        ],
        email: [{ validator: validateEmail, trigger: 'blur' }],
        phone: [
          {
            validator: validatePhoneNumber,
            trigger: 'blur'
          }
        ],
        zipcode: [{ validator: validateZipCode, trigger: 'blur' }],
        other_medium: [{ validator: otherMediumValidate, trigger: 'blur' }],
        ethnic_persuasion: [
          {
            required: true,
            message: 'Choose one ethnic persuasion',
            trigger: 'change'
          }
        ],
        involved: [
          {
            required: true,
            message: 'Please enter number of individuals involved',
            trigger: 'blur'
          }
        ],
        available_at: [{ validator: availableAtValidator, trigger: 'change' }],
        hosting_at: [
          {
            required: true,
            message: 'Please choose the hosting location',
            trigger: 'change'
          }
        ],
        heard_from: [{ validator: heardFromValidator, trigger: 'change' }]
      }
    }
  },
  methods: {
    handleSubmit (name) {
      this.$refs[name].validate(valid => {
        if (valid) {
          this.openIsAgreeModal = true
        } else {
          this.$Notice.error({
            title: 'Submission Error',
            desc: 'Validation errors should be resolved'
          })
          // this.$Message.error("Fail!");
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    agree (is_agreed) {
      this.formValidate.is_agreed = is_agreed
      this.formValidate['survey_meta_data'] = {}
      let data = JSON.stringify(this.formValidate)
      api
        .post('potluck/surveys/', data, { hasPermission: true })
        .then(response => {
          this.isFormSubmitted = true
          this.handleReset('formValidate')
        })
        .catch(error => {
          console.log(error)
          this.handleReset('formValidate')
        })
    }
  },
  beforeMount () {
    let that = this
    api
      .get('potluck/heardfrom/', { hasPermission: true })
      .then(function (response) {
        that.heard_from_options = response.results
      })
      .catch(function (error) {
        console.log(error)
      })
  }
}
</script>

<style lang="scss" scoped>
.agree-modal {
  .ivu-modal-body {
    padding: 20px 30px 20px 40px;
    .heading {
      color: $primary-dark;
      font-size: 14px;
      margin: 0px 0 10px 0;
    }
    .helper {
      color: $warning;
      font-size: 14px;
      margin: 10px 0;
    }
    .content {
      color: $content;
      font-size: 14px;
      li {
        margin-bottom: 5px;
      }
    }
  }
}
.success-card {
  width: 320px;
  margin: auto;
  margin-top: 50px;
  .ivu-icon {
    color: $success;
    font-size: 50px;
    margin-bottom: 10px;
  }
}
.survey-form {
  margin-top: 30px !important;
  padding: 1px;

  .jumbo-text {
    color: $title;
  }
  .description {
    text-align: center;
    vertical-align: middle;
    font-size: 15px;
    color: $content;
    line-height: 23px;
    padding: 10px 12px 10px 0;
    box-sizing: border-box;
  }
  .form {
    border: $border;
    background: $background;
    margin: auto;
    max-width: 900px;
    margin-top: 30px;
    padding: 20px 30px 30px 30px;
    border-radius: 10px;
    .error {
      color: $error;
    }
    .form-header {
      color: $title;
      font-weight: bold;
      font-size: 20px;
      margin: 15px 0;
      text-align: center;
    }
    .form-description {
      color: $sub-content;
      font-weight: normal;
      font-size: 16px;
      margin: 10px 0;
      text-align: center;
    }
    label {
      color: $content;
      font-size: 14px;
    }
    input {
      width: 100%;
    }
  }
}
</style>
