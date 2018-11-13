import React from 'react';
import Link from 'next/link';
import { CardDeck, Card, CardTitle, CardBody, CardSubtitle, CardText, Col, Row } from 'reactstrap';
import { isLevelClear, getAllClearedLevels } from '../services/data';
import * as queryString from 'query-string';
import * as classNames from 'classnames';
import Octicon from 'react-component-octicons';
import Router from 'next/router';
import { fetchApi } from '../services/api';

class LevelList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      stageId: props.stageId,
      totalLevels: 0,
      nextLevelToClear: null,
      name: null
    }
  }

  componentDidMount() {
    fetchApi("/stages/"+this.state.stageId, {}, {}, 'GET')
      .then((response) => {
        // object returned by the API
        let stage = response.data.stage;
        // compute which is the immediate next level user needs to complete
        // this is the (last level cleared) + 1
        let allClearedLevels = getAllClearedLevels(this.state.stageId);
        allClearedLevels = allClearedLevels.map((value, key)=>{
          return Number(value)
        });
        let maxLevelCleared = 0;
        if(allClearedLevels.length > 0){
          maxLevelCleared = Math.max.apply(null, allClearedLevels);
        }
        let nextLevelToClear = maxLevelCleared + 1;

        this.setState({
          nextLevelToClear: nextLevelToClear,
          ...stage
        });
      })
  }

  onLevelCardClick(level) {
    let isCleared = isLevelClear(level, this.state.stageId);
    if(isCleared || this.state.nextLevelToClear == level){
      Router.push("/playLevel?" + queryString.stringify({"level": level, "stageId": this.state.stageId}));
    } else {
      alert("Clear the previous levels before trying out this level.");
    }
  }

  getLevelCardTextMsg(level) {
    let cleared = isLevelClear(level, this.state.stageId);
    if(this.state.nextLevelToClear == level) {
      return "Clear this level to unlock next ones."
    } else if (cleared) {
      return "Yay! You've cleared this one :D"
    } else {
      return "Clear the previous levels to unlock."
    }
  }

  getLevelOcticonName(level) {
    let cleared = isLevelClear(level, this.state.stageId);
    if(this.state.nextLevelToClear == level) {
      return 'key'
    } else if (cleared) {
      return 'checklist'
    } else {
      return 'lock'
    }
  }

  createLevelsList() {
    let levelsList = [];
    for (let i=1; i<=this.state.totalLevels; i++){
      let levelClassNames = classNames('text-white', {
        'bg-success': isLevelClear(i, this.state.stageId),
        'bg-secondary': !isLevelClear(i, this.state.stageId),
        'bg-info': this.state.nextLevelToClear == i
      })
      levelsList.push(
        <Card style={{'marginBottom': '10px'}} key={i} className={levelClassNames} onClick={() => this.onLevelCardClick(i)}>
              <CardBody>
                <Row>
                  <Col xs="11" sm="11" md="11" lg="11" xl="11">
                    <CardTitle> Level {i}</CardTitle>
                    <CardText>{this.getLevelCardTextMsg(i)}</CardText>
                  </Col>
                  <Col xs="1" sm="1" md="1" lg="1" xl="1">
                    <Octicon name={this.getLevelOcticonName(i)} style={{color: 'white', opacity: '0.4'}} zoom="70%"/>
                  </Col>
                </Row>
              </CardBody>
        </Card>
      );
    }
    return levelsList;
  }

  render() {
    return (
      <Col xs="12" sm="12" md="12" lg="12" xl="12" levels={this.state.totalLevels}>
        {this.createLevelsList()}
      </Col>
    )
  }
}

export default LevelList;
