import './App.css';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import Box from "@material-ui/core/Box";

import NavigationBar from "./NavigationBar";
import Landing from "./Landing";
import Tasks from "./Tasks";
import Leaderboard from "./Leaderboard";


const theme = createMuiTheme({
  palette: {
    primary: {
      light: "#ffffff",
      main: "#f5f5f5",
      dark: "#c2c2c2",
    },
    text: {
      primary: "#546e7a",
      secondary: "#9e9e9e"
    }
  }
})


function App() {
  return (
    <div className="App">
      <Router>
        <ThemeProvider theme={theme}>
          <NavigationBar />
          <Box height={theme.spacing(6)}></Box>
          <Switch>
            <Route path="/" exact>
              <Landing />
            </Route>
            <Route path="/tasks">
              <Tasks />
            </Route>
            <Route path="/leaderboard">
              <Leaderboard />
            </Route>
          </Switch>
        </ThemeProvider>
      </Router>
    </div>
  );
}

export default App;
