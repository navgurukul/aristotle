import { Row, Col } from 'reactstrap';
import Router, { withRouter } from 'next/router';

import Layout from '../components/Layout';
import Level from '../components/Level';

const PlayLevel = (props) => (
  <Layout>
    <Row>
      <Level></Level>
    </Row>
  </Layout>
)

export default withRouter(PlayLevel);
