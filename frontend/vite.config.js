import { defineConfig, loadEnv } from 'vite' 
import vue from '@vitejs/plugin-vue'
import path from 'path' // 👈 ajouter ceci

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  console.log('✅ VITE_API_BASE_URL:', env.VITE_API_BASE_URL)

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src') // 👈 alias @ vers src
      }
    },
    define: {
      'import.meta.env': {
        VITE_API_BASE_URL: JSON.stringify(env.VITE_API_BASE_URL)
      }
    }
  }
})
