export const SITE = 'https://tetsujin28.github.io';
export const LANGS = ['en', 'fr', 'es'] as const;
export type Lang = (typeof LANGS)[number];
export const LOCALES: Record<Lang, string> = { en: 'en_US', fr: 'fr_FR', es: 'es_ES' };
export const prefix = (l: Lang) => (l === 'en' ? '' : `/${l}`);
export const homeUrl = (l: Lang) => (l === 'en' ? '/' : `/${l}/`);
export const guideUrl = (app: string, l: Lang) => `${prefix(l)}/${app}/guide/`;
export const abs = (path: string) => SITE + path;
