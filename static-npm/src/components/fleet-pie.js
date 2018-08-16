import React, { Component } from 'react';
import { render } from 'react-dom';

export default class FleetPie extends Component {
    constructor(route, title) {
        super();
        this.state = {
            route: route,
            title: title
        }
    }

    render() {
        return (
            <div className="box" style={{width: 400, height: 350}}>
                <h4 className="subtitle is-4 title-red">Red Line</h4>
                <canvas style={{width: 400, height: 300}}></canvas>
            </div>
        );
    }
}