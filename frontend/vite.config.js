// ./frontend/vite.config.js
/**
 * @file Vite configuration file.
 * This ensures the React plugin is used correctly, which handles the modern JSX transform
 * and prevents the "React is not defined" error.
 */
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})

