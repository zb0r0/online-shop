new Vue({
    el: '#app',
    data: {
        username: '',
        password: '',
        message: ''
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://localhost:5000/login', {
                    username: this.username,
                    password: this.password
                });
                this.message = response.data.message;
            } catch (error) {
                if (error.response && error.response.data) {
                    this.message = error.response.data.message;
                } else {
                    this.message = 'An error occurred';
                }
            }
        }
    }
});
