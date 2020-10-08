Vue.component('correction-view', {
  props: ['token', 'queue'],
  data: function () {
    return {
      message: '',
      errors: [],
      correction: '',
      originalHadith: null,
      queueName: this.queue,
      diff: null,
      addComment: false,
      comment: '',
    };
  },
  created: function () {
    this.loadNextCorrection();
  },
  updated: async function () {
    if (
      this.correction &&
      this.originalHadith === null &&
      !this.loading &&
      this.errors.length === 0
    ) {
      await this.downloadHadith(this.correction.urn);
      if (this.correction.val) {
        this.checkDiff();
      }
      else {
        this.loadOriginal();
      }
    }
  },
  methods: {
    reset: function () {
      this.comment = null;
      this.addComment = false;
      this.errors = [];
      this.correction = null;
      this.loading = false;
      this.originalHadith = null;
      this.diff = null;
    },
    loadOriginal: function () {
      if (this.correction && this.correction.attr && this.originalHadith) {
        this.correction.val = this.originalHadith[this.correction.attr];
      }
      this.checkDiff();
    },
    fetchJsonData: async function (url, body) {
      this.loading = true;
      let resp = null;
      try {
        resp = await fetch(url, {
          method: body ? 'POST' : 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `token ${this.token}`,
          },
          body: body ? JSON.stringify(body) : null
        })
        if (resp.ok) {
          return resp.json();
        }
      }
      finally {
        this.loading = false;
      }
      throw new Error(`Http status ${resp.status}`);
    },
    loadNextCorrection: async function () {
      this.reset();
      try {
        this.correction = await this.fetchJsonData(`/corrections/${this.queueName}`);
        if (!this.correction) {
          this.message = 'No more corrections';
        }
        else {
          this.message = null;
        }
      }
      catch (err) {
        this.errors.push('Error loading correction.');
      }
    },
    downloadHadith: async function (hadithUrn) {
      try {
        const result = await this.fetchJsonData(`/hadtihs/${hadithUrn}`);
        if (result && result.length != 0) {
          for (var i = 0; i < result.hadith.length; i++) {
            if (result.hadith[i].lang === this.correction.lang) {
              this.originalHadith = result.hadith[i];
              break;
            }
          }
        }
      }
      catch (err) {
        this.errors.push('Error loading Hadith.');
      }
    },
    checkDiff: function () {
      const dmp = new diff_match_patch();
      this.diff = dmp.diff_prettyHtml(dmp.diff_main(
        this.originalHadith.body,
        this.correction.val
      )).replaceAll('&para;<br>', '<br/>');
    },
    changeQueue: function (queueName) {
      this.queueName = queueName;
      this.loadNextCorrection();
    },
    accept: function () {
      this.execAction('approve', {
        corrected_value: this.correction.val,
        comment: this.comment,
      })
    },
    reject: function () {
      this.execAction('reject', {
        comment: this.comment,
      });
    },
    skip: function () {
      this.execAction('skip');
    },
    execAction: async function (action, data = {}) {
      try {
        const postData = Object.assign({
          action: action
        }, data)
        const result = await this.fetchJsonData(`/corrections/${this.queueName}/${this.correction.id}`, postData);
        this.message = result.message
        if (result.success) {
          this.loadNextCorrection();
        }
      }
      catch (err) {
        this.errors.push(err.message);
      }
    }
  },
  watch: {
    addComment: function (val) {
      if (!val) this.comment = null;
    }
  }
});

var app = new Vue({
  el: '#app',
});
