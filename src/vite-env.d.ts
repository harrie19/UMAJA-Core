/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly REACT_APP_REALITY_STREAM_URL?: string
  readonly REACT_APP_BACKEND_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
