Vue.component('correction-view', {
    props: ['token'],
    data: function () {
        return {
            message: 'Loading correction...',
            correction: null,
        }
    },
    created: function () {
        this.getNextCorrection();
    },
    methods: {
        getNextCorrection: function () {
            fetch('/corrections', {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `token ${this.token}`,
                },
            })
            .then(resp => resp.ok ? resp : function () { throw new Error(`Http status ${resp.status}`) }())
            .then(resp => resp.json())
            .then(data => {
                if (!data || data.length == 0)
                    alert('no more corrections')
                else {
                    this.message = "loaded";
                    this.correction = data[0];
                }
            })
            .catch(err => alert('something went wrong ' + err.message));
        }
    }
})

var app = new Vue({
    el: '#app'
})