import React from 'react';
import Link from 'next/link';
import { CardDeck, Card, CardTitle, CardBody, CardSubtitle, Col } from 'reactstrap';
import { getStages, getAllClearedLevels } from '../services/data';

class StageList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      stages: []
    }
  }

  componentDidMount() {
    const stages = getStages();
    this.setState({ 'stages': stages['stages'] });
  }

  getClearedLevelCount(stageId) {
    let clearedLevels = getAllClearedLevels(stageId);
    return clearedLevels.length;
  }

  render() {
    return (
      <Col xs="12" sm="12" md="12" lg="12" xl="12">
        {this.state.stages.map((value, key) => (
          <Link href={`/stage?id=`+value.id} key={value.id}>
            <Card style={{'marginBottom': '10px'}}>
              <CardBody>
                <CardTitle>Stage {value.order} ({this.getClearedLevelCount(value.id)}/{value.totalLevels})</CardTitle>
                <CardSubtitle>{value.name}</CardSubtitle>
              </CardBody>
            </Card>
          </Link>
        ))}
      </Col>
    )
  }
}

export default StageList