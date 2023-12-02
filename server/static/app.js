document.addEventListener('DOMContentLoaded', function() {
    const term = new Terminal();
    term.open(document.getElementById('app'));

    const fitAddon = new FitAddon.FitAddon();
    term.loadAddon(fitAddon);
    fitAddon.fit();

    term.write('Welcome to the Python Web IDE!\n');

    new Vue({
        el: '#app',
        template: `
            <div>
                <textarea v-model="code"></textarea>
                <button @click="runCode">Run Code</button>
                <div id="output"></div>
            </div>
        `,
        data() {
            return {
                code: ''
            };
        },
        methods: {
            runCode() {
                term.writeln('Running code...');
                this.$http.post('http://localhost:5000/runcode', { code: this.code })
                    .then(response => {
                        term.writeln(response.body.output);
                    })
                    .catch(error => {
                        term.writeln('Error executing code.');
                        console.error(error);
                    });
            }
        }
    });
});