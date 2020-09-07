Vue.component("correction-view", {
  props: ["token"],
  data: function () {
    return {
      message: "",
      errors: [],
      correction: null,
      originalHadith: null,
      diff: null,
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
      let correction = this.correction;
      await this.loadOriginalHadith(correction.urn);
      this.checkDiff();
    }
  },
  methods: {
    reset: function () {
      this.errors = [];
      this.correction = null;
      this.loading = false;
      this.originalHadith = null;
      this.diff = null;
    },
    fetchJsonData: async function (url, body) {
      const resp = await fetch(url, {
        method: body ? "POST" : "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `token ${this.token}`,
        },
        body: body ? JSON.stringify(body) : null
      })
      if (resp.ok) {
        return resp.json();
      }
      throw new Error(`Http status ${resp.status}`);
    },
    loadNextCorrection: async function () {
      this.reset();
      this.loading = true;
      try {
        const result = await this.fetchJsonData("/corrections");
        this.loading = false;
        if (!result || result.length == 0) this.message = "No more corrections";
        else {
          this.correction = result[0];
        }
      }
      catch (err) {
        this.loading = false;
        this.errors.push("Error loading correction.");
      }
    },
    loadOriginalHadith: async function (hadithUrn) {
      this.loading = true;
      try {
        const result = await this.fetchJsonData("/hadtihs/" + hadithUrn);
        this.loading = false;
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
        this.errors.push("Error loading Hadith.");
        this.loading = false;
      }
    },
    checkDiff: function () {
      const dmp = new diff_match_patch();
      const diff = dmp.diff_main(
        this.originalHadith.body,
        this.correction.val
      );
      this.diff = dmp.diff_prettyHtml(diff);
    },
    accept: async function () {
      try {
        await this.fetchJsonData(`/corrections/${this.correction.id}`, {
          action: 'approve',
          corrected_value: this.correction.val
        });
        this.message = 'accepted the correction';
        this.loadNextCorrection();
      }
      catch (err) {
        this.errors.push(err.message);
      }
    },
    reject: async function () {
      try {
        await this.fetchJsonData(`/corrections/${this.correction.id}`, {
          action: 'reject'
        });
        this.message = 'rejected the correction'
        this.loadNextCorrection();
      }
      catch (err) {
        this.errors.push(err.message);
      }
    },
  },
});

var app = new Vue({
  el: "#app",
});
