import { Row, Col } from 'reactstrap';
import Router, { withRouter } from 'next/router';

import Layout from '../components/Layout';
import LevelList from '../components/LevelList';

const Stage = (props) => (
  <Layout>
    <Row>
      <Col xs="12" sm="12" md="12" lg="12" xl="12"><h1>Levels</h1></Col>
      <LevelList stageId={props.router.query.id}></LevelList>
    </Row>
  </Layout>
)

export default withRouter(Stage);
