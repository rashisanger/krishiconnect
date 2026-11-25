import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiBaseUrl = env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
  const backendOrigin = new URL(apiBaseUrl).origin;

  return {
    plugins: [react()],
    server: {
      proxy: {
        '/api': { target: backendOrigin, changeOrigin: true },
        '/admin': { target: backendOrigin, changeOrigin: true },
      },
    },
  };
});
