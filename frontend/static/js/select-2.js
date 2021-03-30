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
      optionsData: [],
    }
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
      data: this.optionsData
    })
      .on('change', function () {
      vm.$emit('input', select.val())
    })
    select.val(this.value).trigger('change')
  },
  methods: {
    formatOptions() {
      for (let key in this.options) {
        this.optionsData.push({ id: this.options[key].id, text: this.options[key].text })
      }
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})