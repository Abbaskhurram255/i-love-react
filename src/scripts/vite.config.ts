import * as React from "react";
Object.assign(window, React);
import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
})
