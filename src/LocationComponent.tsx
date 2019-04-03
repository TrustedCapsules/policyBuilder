import * as React from "react";

interface LocationComponentState {
    lat: number;
    lon: number;
    radius: number;
}

export default class LocationComponent extends React.Component<{}, LocationComponentState> {
    constructor(props: {}) {
        super(props);
        this.state = {
            lat: 49.2606,
            lon: 123.2460,
            radius: 5
        };
        if ("geolocation" in navigator) { /* geolocation is available */
            navigator.geolocation.getCurrentPosition((position) => {
                this.setState({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                });
            });
        }
    }

    handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({[event.target.name]: event.target.value} as any);
    };

    render() {
        return (<>
            <label> Lat
                <input type="number" name="lat" value={this.state.lat} onChange={this.handleChange}/>
            </label>
            <label> Lon
                <input type="number" name="lon" value={this.state.lon} onChange={this.handleChange}/>
            </label>
            <label> Radius
                <input type="number" name="radius" value={this.state.radius} onChange={this.handleChange}/>
            </label>
        </>);

    }
}

