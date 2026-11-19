import type { Lang } from './site';

export type App = {
  name: string;
  accent: string;
  icon: string;
  title: Record<Lang, string>;
  desc: Record<Lang, string>;
};

export const APPS: Record<string, App> = {
  bandua: {
    name: 'Bandua', accent: '#f39a3c', icon: 'bandua-icon.png',
    title: { en: 'Bandua user guide', fr: "Bandua, mode d'emploi", es: 'Bandua, manual de uso' },
    desc: {
      en: 'Complete user guide for Bandua, the free app that offloads camera cards and verifies every copy by hash. Step by step, with annotated screenshots.',
      fr: "Mode d'emploi complet de Bandua, l'application gratuite qui décharge les cartes caméra et vérifie chaque copie par hash. Pas à pas, avec des captures d'écran annotées.",
      es: 'Manual de uso completo de Bandua, la aplicación gratuita que vuelca las tarjetas de cámara y verifica cada copia por hash. Paso a paso, con capturas de pantalla anotadas.',
    },
  },
  lugus: {
    name: 'Lugus Transfer', accent: '#39c6ff', icon: 'lugus-icon.png',
    title: { en: 'Lugus Transfer user guide', fr: "Lugus Transfer, mode d'emploi", es: 'Lugus Transfer, manual de uso' },
    desc: {
      en: 'Complete user guide for Lugus Transfer, the free app that sends footage straight from one computer to another with a link and a code, verified on arrival. Step by step, with annotated screenshots.',
      fr: "Mode d'emploi complet de Lugus Transfer, l'application gratuite qui envoie les rushes directement d'un ordinateur à l'autre avec un lien et un code, vérifiés à l'arrivée. Pas à pas, avec des captures d'écran annotées.",
      es: 'Manual de uso completo de Lugus Transfer, la aplicación gratuita que envía el material directamente de un ordenador a otro con un enlace y un código, verificado a la llegada. Paso a paso, con capturas de pantalla anotadas.',
    },
  },
  companion: {
    name: 'Bandua MHL Companion', accent: '#6cb6ff', icon: 'companion-icon.png',
    title: { en: 'Bandua MHL Companion user guide', fr: "Bandua MHL Companion, mode d'emploi", es: 'Bandua MHL Companion, manual de uso' },
    desc: {
      en: 'Complete user guide for Bandua MHL Companion, the free app that checks received footage against its MHL files. Step by step, with annotated screenshots.',
      fr: "Mode d'emploi complet de Bandua MHL Companion, l'application gratuite qui contrôle les rushes reçus d'après leurs fichiers MHL. Pas à pas, avec des captures d'écran annotées.",
      es: 'Manual de uso completo de Bandua MHL Companion, la aplicación gratuita que controla el material recibido con sus archivos MHL. Paso a paso, con capturas de pantalla anotadas.',
    },
  },
  ataecina: {
    name: 'Ataecina', accent: '#e2c043', icon: 'ataecina-icon.png',
    title: { en: 'Ataecina user guide', fr: "Ataecina, mode d'emploi", es: 'Ataecina, manual de uso' },
    desc: {
      en: 'Complete user guide for Ataecina, the free app that recovers footage from formatted or damaged camera cards and repairs broken MOV and MP4 files. With the setup of untrunc, FFmpeg and PhotoRec.',
      fr: "Mode d'emploi complet d'Ataecina, l'application gratuite qui récupère des rushes sur des cartes caméra formatées ou endommagées et répare les fichiers MOV et MP4 cassés. Avec l'installation d'untrunc, FFmpeg et PhotoRec.",
      es: 'Manual de uso completo de Ataecina, la aplicación gratuita que recupera material de tarjetas de cámara formateadas o dañadas y repara archivos MOV y MP4 rotos. Con la instalación de untrunc, FFmpeg y PhotoRec.',
    },
  },
};

export const UI: Record<Lang, { back: (n: string) => string; close: string }> = {
  en: { back: n => `Back to ${n}`, close: 'Close' },
  fr: { back: n => `Retour à ${n}`, close: 'Fermer' },
  es: { back: n => `Volver a ${n}`, close: 'Cerrar' },
};
