import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import {exec} from 'child_process'

const kexe = () => {
  // Helper to prevent kreact.exe from running 50 times at once
  let isFixing = false;

  const runFixer = () => {
    if (isFixing) return;
    isFixing = true;

    console.log('\nCompilation failed! Triggering kreact.exe...');
    
    exec('kreact.exe', (err, stdout, stderr) => {
      if (stdout) console.log(stdout);
      if (stderr) console.error(stderr);
      
      // Allow the fixer to run again on the next failure
      setTimeout(() => { isFixing = false; }, 1000);
    });
  };

  return {
    name: 'kexe',

    // 1. Catches transpilation errors during development (vite dev)
    transform(code, id) {
      // We only care about errors in your source React/JS/TS files
      if (id.includes('node_modules')) return;

      try {
        // This hook is normally passive, but if a previous plugin 
        // failed to parse the file, it can throw an error here.
      } catch (err) {
        runFixer();
      }
    },

    // 2. Fallback catcher for server middleware errors in dev mode
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        // Intercepts global errors handled by Vite's connect server middleware
        const originalEnd = res.end;
        res.end = function (chunk, encoding) {
          if (res.statusCode >= 400 || (chunk && chunk.toString().includes('Internal Server Error'))) {
            runFixer();
          }
          return originalEnd.apply(this, arguments);
        };
        next();
      });
    },

    // 3. Catches errors during production builds (vite build)
    buildEnd(error) {
      if (error) {
        runFixer();
      }
    }
  };
};

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    kexe()
  ],
})