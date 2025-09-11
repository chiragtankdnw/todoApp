import React, { Component } from "react";
import axios from "axios";

class BlogSummaries extends Component {
    constructor(props) {
        super(props);
        this.state = {
            blogSummaries: []
        };
    }

    componentDidMount() {
        this.fetchBlogSummaries();
    }

    fetchBlogSummaries = () => {
        axios
            .get("/api/blog-summaries/")
            .then(res => this.setState({ blogSummaries: res.data }))
            .catch(err => console.log(err));
    };

    render() {
        const { blogSummaries } = this.state;

        return (
            <div className="blog-summaries-section mt-4">
                <h4 className="text-center mb-3">Latest Blog Post Summaries</h4>
                {blogSummaries.length > 0 ? (
                    <div className="blog-summaries-list">
                        {blogSummaries.map(summary => (
                            <div key={summary.id} className="card mb-3">
                                <div className="card-body">
                                    <h5 className="card-title">
                                        <a href={summary.url} target="_blank" rel="noopener noreferrer">
                                            {summary.title}
                                        </a>
                                    </h5>
                                    <div className="card-subtitle mb-2 text-muted">
                                        <small>
                                            Published: {summary.date_published}
                                            {summary.location_timezone && ` | ${summary.location_timezone}`}
                                        </small>
                                    </div>
                                    <p className="card-text" style={{whiteSpace: 'pre-line'}}>
                                        {summary.summary}
                                    </p>
                                    {summary.tags && (
                                        <div className="tags">
                                            <small className="text-info">
                                                Tags: {summary.tags}
                                            </small>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="text-center text-muted">No blog summaries available.</p>
                )}
            </div>
        );
    }
}

export default BlogSummaries;