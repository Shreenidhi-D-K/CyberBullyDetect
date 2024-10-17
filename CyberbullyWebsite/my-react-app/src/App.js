import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Components/Home";
import NoPage from "./Components/NoPage";

const App=()=>{
  return(
    // <h1>Welcome to react Application</h1>
    <>
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="Home" element={<Home/>} />
          <Route path="*" element={<NoPage />} />
      </Routes>
    </BrowserRouter>
    </>
  )
}
export default App;
