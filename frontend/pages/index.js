import { Row, Col } from 'reactstrap';

import Layout from '../components/Layout';
import StageList from '../components/StageList';

const Index = () => (
  <Layout>
    <Row>
      <Col xs="12" sm="12" md="12" lg="12" xl="12"><h1>Stages</h1></Col>
      <StageList></StageList>
    </Row>
  </Layout>
)

export default Index
