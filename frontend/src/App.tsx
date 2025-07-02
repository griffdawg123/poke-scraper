import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { MantineProvider } from '@mantine/core'
import { BrowserRouter } from 'react-router-dom'

function App() {

  return (
    <BrowserRouter>
      <MantineProvider withGlobalStyles withNormalizeCSS>
        <div className="App">
          <header className="App-header">
            <img src={viteLogo} className="logo vite" alt="Vite logo" />
            <img src={reactLogo} className="logo react" alt="React logo" />
            <h1>Vite + React</h1>
            <p>
              Edit <code>src/App.tsx</code> and save to test HMR
            </p>
          </header>
        </div>
      </MantineProvider>
    </BrowserRouter>
  )
}

export default App
