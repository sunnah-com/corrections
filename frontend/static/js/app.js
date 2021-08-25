Vue.component('correction-view', {
  props: ['token', 'queue'],
  data: function () {
    return {
      message: '',
      isError: false,
      loading: true,
      correction: '',
      originalHadith: null,
      queueName: this.queue,
      diff: null,
      addModeratorComment: false,
      queues: [],
    };
  },
  mounted: function () {
    this.getQueues();
  },
  created: function () {
    this.loadNextCorrection();
  },
  updated: async function () {
    if (
      this.correction &&
      this.originalHadith === null &&
      !this.loading && 
      !this.isError
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
      this.addModeratorComment = false;
      this.correction = null;
      this.loading = true;
      this.originalHadith = null;
      this.diff = null;
    },
    alert: function (message, isError) {
      this.message = message;
      this.isError = isError;
    },
    loadOriginal: function () {
      if (this.correction && this.correction.attr && this.originalHadith) {
        this.correction.val = this.originalHadith[this.correction.attr];
      }
      this.checkDiff();
    },
    fetchJsonData: async function (url, body) {
      this.loading = true;
      let resp = null
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
          this.alert('No more corrections.', false);
        }
      }
      catch (err) {
        this.alert('Error loading correction.', true);
      }
    },
    downloadHadith: async function (hadithUrn) {
      try {
        const result = await this.fetchJsonData(`/hadiths/${hadithUrn}`);
        /*
        {
        "collection": "bukhari",
        "bookNumber": "1",
        "chapterId": "1",
        "hadithNumber": "1",
        "hadith": [{
              "lang": "en",
              "chapterNumber": "1",
              "chapterTitle": "title goes here",
              "urn": 10,
              "body": "hadith text goes here",
              "grades": [{
                      "graded_by": "authority",
                      "grade": "Sahih"
                }]
          }]
        }*/
        if (result && result.length != 0) {
          // TODO: move this logic to python
          // flatten the hadith by plucking the lang specific data 
          // and merge it with the root
          for (var i = 0; i < result.hadith.length; i++) {
            if (result.hadith[i].lang === this.correction.lang) {
              let hadith = Object.assign({}, result, result.hadith[i]);
              // delete data for other languages
              delete hadith.hadith;
              this.originalHadith = hadith;
              break;
            }
          }
        }
      }
      catch (err) {
        this.alert('Error loading hadith.', true);
      }
    },
    getQueues: async function () {
      try {
        const result = await this.fetchJsonData(`/queues/`);
        this.queues = result
      }
      catch (err) {
        this.alert('Error fetching queues.', true);
      }
    },
    checkDiff: function () {
      if (this.originalHadith == null || this.correction == null) return;

      let originalVal = this.originalHadith[this.correction.attr] || '';
      let correctedVal = this.correction.val;
      let dmp = new diff_match_patch();
      let diff = dmp.diff_main(originalVal, correctedVal);
      this.diff = dmp.diff_prettyHtml(diff).replaceAll('&para;<br>', '<br/>');
    },
    changeQueue: function (queueName) {
      this.queueName = queueName;
      this.loadNextCorrection();
    },
    accept: function () {
      this.execAction('approve', {
        corrected_val: this.correction.val,
        version: this.correction.version,
        emailTemplate: this.emailTemplate,
      })
    },
    reject: function () {
      this.execAction('reject', {
        version: this.correction.version,
        emailTemplate: this.emailTemplate,
      });
    },
    skip: function () {
      this.execAction('skip', {
        version: this.correction.version,
      });
    },
    move: function (queueName) {
      this.execAction('move', {
        version: this.correction.version,
        new_queue_name: queueName,
      });
    },
    execAction: async function (action, data = {}) {
      try {
        const postData = Object.assign({
          action: action
        }, data)
        const result = await this.fetchJsonData(`/corrections/${this.queueName}/${this.correction.id}`, postData);
        this.alert(result.message, !result.success);

        if (result.success) {
          this.loadNextCorrection();
        }
      }
      catch (err) {
        this.alert(err.message, true);
      }
    }
  },
  watch: {
    addModeratorComment: function (val) {
      this.emailTemplate = val ? originalEmailTemplate : '';
    }
  }
});

var app = new Vue({
  el: '#app',
});
