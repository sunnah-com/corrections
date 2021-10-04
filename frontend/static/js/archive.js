Vue.component('archive-view', {
    data: function () {
        return {
            records: [],
            search: '',
        }
    },
    methods: {
        async getRecords() {
            this.records = await fetchJsonData('/api/archive');
        },
        async handleRevert(record) {
            // TODO: post revert to backend and reload the page
        }
    },
    mounted: function () {
        this.getRecords();
    }
})
