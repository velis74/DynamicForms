import { defineConfig } from 'vitepress';

function appendBasePath(basePath: string, items: Array<{text: string, link: string}>) {
  return items.map(item => ({
    ...item,
    link: `/${basePath}/${item.link.replace(/^\//, '')}`
  }));
}

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: 'DynamicForms',
  description: 'Django DRF REST to HTML forms, tables and dialogs',
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: '/examples/markdown-examples' },
      { text: 'Reference', link: '/reference/index' }
    ],

    sidebar: {
      '/examples/': [{
        text: 'Examples',
        items: appendBasePath('examples', [
          { text: 'Markdown Examples', link: 'markdown-examples' },
          { text: 'Runtime API Examples', link: 'api-examples' }
        ])
      }],
      '/reference/': [
        {
          text: 'Reference',
          items: appendBasePath('reference', [
            { text: 'Index', link: 'index' },
            { text: 'Hiding titlebar & Navbar', link: 'hiding_titlebar_and_navbar' },
            { text: 'Dialog size', link: 'dialog-size' },
            { text: 'Form layout', link: 'layout' }
          ])
        }]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/velis74/DynamicForms' }
    ]
  }
});
