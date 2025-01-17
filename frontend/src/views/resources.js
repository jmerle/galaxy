import React, { Component } from "react";
import { NavLink } from "react-router-dom";

class Resources extends Component {
  render() {
    return (
      <div className="content">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-12">
              {this.props.is_game_released && this.props.episode_info && (
                <div className="card">
                  <div className="header">
                    <h4 className="title">Game Specifications</h4>
                  </div>
                  <div className="content">
                    <p className="text-center">
                      <a
                        type="button"
                        className="btn btn-info btn-fill text-center"
                        href={`https://releases.battlecode.org/specs/${this.props.episode_info.artifact_name}/${this.props.episode_info.release_version_public}/specs.md.html`}
                      >
                        Specifications for {this.props.episode_name_long}!
                      </a>
                    </p>
                    <p className="text-center">
                      <a
                        type="button"
                        className="btn btn-info btn-fill text-center"
                        href={`https://releases.battlecode.org/javadoc/${this.props.episode_info.artifact_name}/${this.props.episode_info.release_version_public}/index.html`}
                      >
                        Javadocs for {this.props.episode_name_long}!
                      </a>
                    </p>
                  </div>
                </div>
              )}
              <div className="card">
                <div className="header">
                  <h4 className="title">Coding Resources</h4>
                </div>
                <div className="content">
                  <p>
                    If you're just starting out, check out the{" "}
                    <NavLink
                      to={`/${this.props.episode}/getting-started`}
                      style={{ fontWeight: 700 }}
                    >
                      getting started
                    </NavLink>{" "}
                    page!
                  </p>
                  <p>For more helpful resources while coding, see:</p>
                  <p className="text-center">
                    <a
                      type="button"
                      className="btn btn-info btn-fill text-center"
                      href={`/${this.props.episode}/common-issues`}
                    >
                      Common Issues
                    </a>
                  </p>
                  <p className="text-center">
                    <a
                      type="button"
                      className="btn btn-info btn-fill text-center"
                      href={`/${this.props.episode}/debugging-tips`}
                    >
                      Debugging Tips
                    </a>
                  </p>
                </div>
              </div>
              <div className="card">
                <div className="header">
                  <h4 className="title">Third-party Tools</h4>
                </div>
                <div className="content">
                  <p>
                    The tools below were made by contestants! They haven't been
                    tested by the devs, but might prove to be very helpful in
                    developing your bot.
                  </p>
                  <p>
                    If you make a new tool that could be useful to others,
                    please post it in the{" "}
                    <a href="https://discord.gg/N86mxkH">
                      #open-source channel
                    </a>{" "}
                    on the Discord. Everyone will love you!!
                  </p>
                  <ul>
                    <li>There is nothing here yet...</li>
                  </ul>
                </div>
              </div>

              <div className="card">
                <div className="header">
                  <h4 className="title">Lectures</h4>
                </div>
                <div className="content">
                  <p>
                    {this.props.episode_name_long} will be holding lectures,
                    where a dev will be going over possible strategy, coding up
                    an example player, answering questions, etc. Lectures are
                    streamed on Twitch .
                    {/* every weekday the first two weeks of IAP. */}
                    <i>More details coming soon!</i>
                  </p>
                  <p>
                    All lectures are streamed live on{" "}
                    <a href="https://twitch.tv/mitbattlecode">
                      our Twitch account
                    </a>
                    , and are later uploaded to{" "}
                    <a href="https://youtube.com/channel/UCOrfTSnyimIXfYzI8j_-CTQ">
                      our YouTube channel
                    </a>
                    .
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Resources;
