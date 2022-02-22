module.exports = {
  head: [
    ['script', {src: '../../../df-components.js'}],
    ['script', {src: '../../../df-components-vendors.js'}],
    ['link', {rel: 'stylesheet', href: '../../../df-components.css'}],
    ['link', {rel: 'stylesheet', href: '../../../df-components-vendor.css'}]
  ],
  title: 'Documentation title',
  description: 'Start writing documentation',
  themeConfig: {
    sidebar: {
      '/pages/': getSidebar(),
      '/': getSidebar(),
    }
  },
}

function getSidebar() {
  return [
    {
      text: 'Demo',
      children: [
        {text: 'Examples', link: '/pages/examples/index'},
        {text: 'Descriptions', link: '/pages/descriptions/index'},
        {text: 'Vue Components', link: '/pages/vue-components/index'},
      ]
    },
  ];
}
