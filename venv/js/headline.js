class Headline extends React.Component {
    constructor() {
        super(props);
        this.state = {clicked: false, hidden: false};
    }

    onClick() {
        let win = window.open(this.props.url, '_blank');
        win.focus();
        this.setState({clicked: true, hidden: false});
    }

    render() {
        let colour = this.state.clicked ? '#53161a' : '#5a72ff';

        return (
            <div className="headlines">
                <h4> <a onClick={this.onClick.bind(this)} style={{color: colour}}> {this.props.title} </a> </h4>

                <span className="summary" style={{color: colour}} hidden={this.state.hidden}> {this.props.excerpt} </span>

                <span className="timestamp"><small> {this.props.timestamp} </small></span>
            </div>
        );
    }
}