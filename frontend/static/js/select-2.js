Vue.component('select-2', {
  template: '<select v-bind:name="name" class="form-control" v-bind:multiple="multiple"></select>',
  props: {
    name: '',
    options: {
      Object
    },
    value: null,
    multiple: {
      Boolean,
      default: false

    }
  },
  data() {
    return {
      select2data: [],
      select2Instance: null
    }
  },
  watch: {
    // value (val) {
      // console.log(val);
      // this.select2Instance.val(this.value).trigger('change')
    // }
  },
  mounted() {
    this.formatOptions()
    let vm = this
    let select = $(this.$el)
    select
      .select2({
      placeholder: 'Select here',
      theme: 'bootstrap',
      width: '100%',
      allowClear: true,
      data: this.select2data
    })
      .on('change', function () {
      vm.$emit('input', select.val())
    })
    select.val(this.value).trigger('change')
    // this.select2Instance = select;
  },
  methods: {
    formatOptions() {
      for (let key in this.options) {
        this.select2data.push({ id: this.options[key].id, text: this.options[key].text })
      }
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})