Vue.component("correction-view", {
  props: ["token"],
  data: function () {
    return {
      message: "",
      correction: { data: null, loading: false, errors: [] },
      originalHadith: { data: null, loading: false, errors: [] },
      diff: null,
    };
  },
  created: function () {
    this.loadNextCorrection();
  },
  updated: function () {
    if (
      this.correction.data &&
      this.originalHadith.data === null &&
      !this.originalHadith.loading &&
      this.originalHadith.errors.length === 0
    ) {
      let correction = this.correction.data;
      this.loadOriginalHadith(correction.urn).then(() => {
        this.checkDiff();
      });
    }
  },
  methods: {
    fetchJsonData: function (url, token) {
      return fetch(url, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `token ${token}`,
        },
      })
        .then((resp) =>
          resp.ok
            ? resp
            : (function () {
                throw new Error(`Http status ${resp.status}`);
              })()
        )
        .then((resp) => resp.json());
    },
    loadNextCorrection: function () {
      this.correction.loading = true;
      this.fetchJsonData("/corrections", this.token)
        .then((data) => {
          this.correction.loading = false;
          if (!data || data.length == 0) this.message = "No more corrections";
          else {
            this.correction.data = data[0];
          }
        })
        .catch((err) => {
          this.correction.loading = false;
          this.correction.errors.push("Error loading correction.");
        });
    },
    loadOriginalHadith: function (hadithUrn) {
      this.originalHadith.loading = true;
      return this.fetchJsonData("/hadtihs/" + hadithUrn, this.token)
        .then((data) => {
          this.originalHadith.loading = false;
          if (data && data.length != 0) {
            this.originalHadith.data = data;
            for (var i = 0; i < data.hadith.length; i++) {
              if (data.hadith[i].lang === this.correction.data.lang) {
                this.originalHadith.data.relevantHadith = data.hadith[i];
              }
            }
          }
        })
        .catch((err) => {
          this.originalHadith.errors.push("Error loading Hadith.");
          this.originalHadith.loading = false;
        });
    },
    checkDiff: function () {
      var dmp = new diff_match_patch();
      var diff = dmp.diff_main(
        this.correction.data.val,
        this.originalHadith.data.relevantHadith.body
      );
      this.diff = dmp.diff_prettyHtml(diff);
    },
    accept: function () {
      // TODO: implement
    },
    reject: function () {
      // TODO: implement
    },
  },
});

var app = new Vue({
  el: "#app",
});
