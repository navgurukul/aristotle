import 'bootstrap/dist/css/bootstrap.css';
import { Navbar, NavbarBrand, Container } from 'reactstrap';

const Layout = (props) => (
    <div className="app">
        <Navbar color="primary" dark>
          <NavbarBrand href="/">Shakuntla Devi</NavbarBrand>
        </Navbar>
        <Container>
          {props.children}
        </Container>
    </div>
)

export default Layout;
