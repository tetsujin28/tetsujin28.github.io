import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://tetsujin28.github.io',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  integrations: [sitemap({ i18n: { defaultLocale: 'en', locales: { en: 'en-US', fr: 'fr-FR', es: 'es-ES' } } })],
  devToolbar: { enabled: false },
});
