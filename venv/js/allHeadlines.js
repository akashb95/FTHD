class allHeadlines extends React.Component {
    constructor() {
        super(props);
        this.state = {expanded: true}
    }

    toggleExpand() {
        this.setState({expanded: !expanded});
    }

    render() {
        let headlines = this.props.headlines();

        return {
        <div className="headlines">
            {}
        </div>
        }
    }
}