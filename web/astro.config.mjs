// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://espanaendatos.bocal.online",
  trailingSlash: "always",
  // Antes en vercel.json; en GitHub Pages son páginas de redirección estáticas.
  redirects: {
    "/espana": "/",
    "/historias": "/notas/",
  },
});
