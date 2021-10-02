Vue.component('archive-view', {
    props: ['token'],
    data: function () {
        return {
            records: [],
            search: '',
        }
    },
    methods: {
        async getRecords() {
            this.records = await fetchJsonData(this.token, '/api/archive');
        },
        async handleRevert(record) {
            // TODO: post revert to backend and reload the page
        }
    },
    mounted: function () {
        this.getRecords();
    }
})
