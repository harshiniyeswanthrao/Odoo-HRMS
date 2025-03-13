// hello_widget.js
odoo.define('hello_owl.HelloWidget', function (require) {
    "use strict";

    const { Component } = require('owl');
    const { useState } = require('owl.hooks');

    class HelloWidget extends Component {
        constructor() {
            super(...arguments);
            this.state = useState({
                message: "Hello, Odoo with Owl!",
            });
        }

        static template = "hello_owl.HelloWidget";
    }

    return HelloWidget;
});
