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
    },
    mounted: function () {
        this.getRecords();
    }
})
