import { c as create_ssr_component, s as subscribe, b as each, d as add_attribute, e as escape } from "../../chunks/ssr.js";
import { p as page } from "../../chunks/stores.js";
const css = {
  code: ".layout.svelte-13bvrgb.svelte-13bvrgb{display:flex;min-height:100vh}.sidebar.svelte-13bvrgb.svelte-13bvrgb{width:240px;background:var(--gray-800);color:white;display:flex;flex-direction:column;flex-shrink:0}.logo.svelte-13bvrgb.svelte-13bvrgb{padding:1.25rem;display:flex;align-items:center;gap:0.75rem;border-bottom:1px solid var(--gray-700)}.logo-icon.svelte-13bvrgb.svelte-13bvrgb{font-size:1.75rem}.logo.svelte-13bvrgb h1.svelte-13bvrgb{font-size:1rem;font-weight:600;color:white}.nav.svelte-13bvrgb.svelte-13bvrgb{flex:1;padding:0.75rem 0}.nav-item.svelte-13bvrgb.svelte-13bvrgb{display:flex;align-items:center;gap:0.75rem;padding:0.75rem 1.25rem;color:var(--gray-300);transition:all 0.2s;border-left:3px solid transparent}.nav-item.svelte-13bvrgb.svelte-13bvrgb:hover{background:var(--gray-700);color:white}.nav-item.active.svelte-13bvrgb.svelte-13bvrgb{background:var(--gray-700);color:white;border-left-color:var(--primary)}.nav-icon.svelte-13bvrgb.svelte-13bvrgb{font-size:1.125rem}.nav-label.svelte-13bvrgb.svelte-13bvrgb{font-size:0.875rem}.main.svelte-13bvrgb.svelte-13bvrgb{flex:1;overflow-x:hidden}.content.svelte-13bvrgb.svelte-13bvrgb{padding:1.5rem;max-width:1400px;margin:0 auto}@media(max-width: 768px){.sidebar.svelte-13bvrgb.svelte-13bvrgb{width:60px}.logo.svelte-13bvrgb h1.svelte-13bvrgb,.nav-label.svelte-13bvrgb.svelte-13bvrgb{display:none}.nav-item.svelte-13bvrgb.svelte-13bvrgb{justify-content:center;padding:0.75rem}.content.svelte-13bvrgb.svelte-13bvrgb{padding:1rem}}",
  map: '{"version":3,"file":"+layout.svelte","sources":["+layout.svelte"],"sourcesContent":["<script lang=\\"ts\\">import \\"../app.css\\";\\nimport { page } from \\"$app/stores\\";\\nconst navItems = [\\n  { path: \\"/\\", label: \\"\\\\u4EEA\\\\u8868\\\\u76D8\\", icon: \\"\\\\u{1F4CA}\\" },\\n  { path: \\"/properties\\", label: \\"\\\\u623F\\\\u6E90\\\\u7BA1\\\\u7406\\", icon: \\"\\\\u{1F3E0}\\" },\\n  { path: \\"/tenants\\", label: \\"\\\\u79DF\\\\u5BA2\\\\u7BA1\\\\u7406\\", icon: \\"\\\\u{1F464}\\" },\\n  { path: \\"/contracts\\", label: \\"\\\\u5408\\\\u540C\\\\u7BA1\\\\u7406\\", icon: \\"\\\\u{1F4DD}\\" },\\n  { path: \\"/bills\\", label: \\"\\\\u8D26\\\\u5355\\\\u7BA1\\\\u7406\\", icon: \\"\\\\u{1F4B0}\\" },\\n  { path: \\"/repairs\\", label: \\"\\\\u7EF4\\\\u4FEE\\\\u62A5\\\\u4E8B\\", icon: \\"\\\\u{1F527}\\" },\\n  { path: \\"/renewals\\", label: \\"\\\\u7EED\\\\u7EA6\\\\u7BA1\\\\u7406\\", icon: \\"\\\\u{1F504}\\" }\\n];\\nlet currentPath = \\"\\";\\n$: currentPath = $page.url.pathname;\\nfunction isActive(path) {\\n  if (path === \\"/\\") return currentPath === \\"/\\";\\n  return currentPath.startsWith(path);\\n}\\n<\/script>\\r\\n\\r\\n<div class=\\"layout\\">\\r\\n\\t<aside class=\\"sidebar\\">\\r\\n\\t\\t<div class=\\"logo\\">\\r\\n\\t\\t\\t<span class=\\"logo-icon\\">🏢</span>\\r\\n\\t\\t\\t<h1>房产管理系统</h1>\\r\\n\\t\\t</div>\\r\\n\\t\\t<nav class=\\"nav\\">\\r\\n\\t\\t\\t{#each navItems as item}\\r\\n\\t\\t\\t\\t<a href={item.path} class=\\"nav-item\\" class:active={isActive(item.path)}>\\r\\n\\t\\t\\t\\t\\t<span class=\\"nav-icon\\">{item.icon}</span>\\r\\n\\t\\t\\t\\t\\t<span class=\\"nav-label\\">{item.label}</span>\\r\\n\\t\\t\\t\\t</a>\\r\\n\\t\\t\\t{/each}\\r\\n\\t\\t</nav>\\r\\n\\t</aside>\\r\\n\\t<main class=\\"main\\">\\r\\n\\t\\t<div class=\\"content\\">\\r\\n\\t\\t\\t<slot />\\r\\n\\t\\t</div>\\r\\n\\t</main>\\r\\n</div>\\r\\n\\r\\n<style>\\r\\n\\t.layout {\\r\\n\\t\\tdisplay: flex;\\r\\n\\t\\tmin-height: 100vh;\\r\\n\\t}\\r\\n\\r\\n\\t.sidebar {\\r\\n\\t\\twidth: 240px;\\r\\n\\t\\tbackground: var(--gray-800);\\r\\n\\t\\tcolor: white;\\r\\n\\t\\tdisplay: flex;\\r\\n\\t\\tflex-direction: column;\\r\\n\\t\\tflex-shrink: 0;\\r\\n\\t}\\r\\n\\r\\n\\t.logo {\\r\\n\\t\\tpadding: 1.25rem;\\r\\n\\t\\tdisplay: flex;\\r\\n\\t\\talign-items: center;\\r\\n\\t\\tgap: 0.75rem;\\r\\n\\t\\tborder-bottom: 1px solid var(--gray-700);\\r\\n\\t}\\r\\n\\r\\n\\t.logo-icon {\\r\\n\\t\\tfont-size: 1.75rem;\\r\\n\\t}\\r\\n\\r\\n\\t.logo h1 {\\r\\n\\t\\tfont-size: 1rem;\\r\\n\\t\\tfont-weight: 600;\\r\\n\\t\\tcolor: white;\\r\\n\\t}\\r\\n\\r\\n\\t.nav {\\r\\n\\t\\tflex: 1;\\r\\n\\t\\tpadding: 0.75rem 0;\\r\\n\\t}\\r\\n\\r\\n\\t.nav-item {\\r\\n\\t\\tdisplay: flex;\\r\\n\\t\\talign-items: center;\\r\\n\\t\\tgap: 0.75rem;\\r\\n\\t\\tpadding: 0.75rem 1.25rem;\\r\\n\\t\\tcolor: var(--gray-300);\\r\\n\\t\\ttransition: all 0.2s;\\r\\n\\t\\tborder-left: 3px solid transparent;\\r\\n\\t}\\r\\n\\r\\n\\t.nav-item:hover {\\r\\n\\t\\tbackground: var(--gray-700);\\r\\n\\t\\tcolor: white;\\r\\n\\t}\\r\\n\\r\\n\\t.nav-item.active {\\r\\n\\t\\tbackground: var(--gray-700);\\r\\n\\t\\tcolor: white;\\r\\n\\t\\tborder-left-color: var(--primary);\\r\\n\\t}\\r\\n\\r\\n\\t.nav-icon {\\r\\n\\t\\tfont-size: 1.125rem;\\r\\n\\t}\\r\\n\\r\\n\\t.nav-label {\\r\\n\\t\\tfont-size: 0.875rem;\\r\\n\\t}\\r\\n\\r\\n\\t.main {\\r\\n\\t\\tflex: 1;\\r\\n\\t\\toverflow-x: hidden;\\r\\n\\t}\\r\\n\\r\\n\\t.content {\\r\\n\\t\\tpadding: 1.5rem;\\r\\n\\t\\tmax-width: 1400px;\\r\\n\\t\\tmargin: 0 auto;\\r\\n\\t}\\r\\n\\r\\n\\t@media (max-width: 768px) {\\r\\n\\t\\t.sidebar {\\r\\n\\t\\t\\twidth: 60px;\\r\\n\\t\\t}\\r\\n\\r\\n\\t\\t.logo h1,\\r\\n\\t\\t.nav-label {\\r\\n\\t\\t\\tdisplay: none;\\r\\n\\t\\t}\\r\\n\\r\\n\\t\\t.nav-item {\\r\\n\\t\\t\\tjustify-content: center;\\r\\n\\t\\t\\tpadding: 0.75rem;\\r\\n\\t\\t}\\r\\n\\r\\n\\t\\t.content {\\r\\n\\t\\t\\tpadding: 1rem;\\r\\n\\t\\t}\\r\\n\\t}\\r\\n</style>\\r\\n"],"names":[],"mappings":"AA0CC,qCAAQ,CACP,OAAO,CAAE,IAAI,CACb,UAAU,CAAE,KACb,CAEA,sCAAS,CACR,KAAK,CAAE,KAAK,CACZ,UAAU,CAAE,IAAI,UAAU,CAAC,CAC3B,KAAK,CAAE,KAAK,CACZ,OAAO,CAAE,IAAI,CACb,cAAc,CAAE,MAAM,CACtB,WAAW,CAAE,CACd,CAEA,mCAAM,CACL,OAAO,CAAE,OAAO,CAChB,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,GAAG,CAAE,OAAO,CACZ,aAAa,CAAE,GAAG,CAAC,KAAK,CAAC,IAAI,UAAU,CACxC,CAEA,wCAAW,CACV,SAAS,CAAE,OACZ,CAEA,oBAAK,CAAC,iBAAG,CACR,SAAS,CAAE,IAAI,CACf,WAAW,CAAE,GAAG,CAChB,KAAK,CAAE,KACR,CAEA,kCAAK,CACJ,IAAI,CAAE,CAAC,CACP,OAAO,CAAE,OAAO,CAAC,CAClB,CAEA,uCAAU,CACT,OAAO,CAAE,IAAI,CACb,WAAW,CAAE,MAAM,CACnB,GAAG,CAAE,OAAO,CACZ,OAAO,CAAE,OAAO,CAAC,OAAO,CACxB,KAAK,CAAE,IAAI,UAAU,CAAC,CACtB,UAAU,CAAE,GAAG,CAAC,IAAI,CACpB,WAAW,CAAE,GAAG,CAAC,KAAK,CAAC,WACxB,CAEA,uCAAS,MAAO,CACf,UAAU,CAAE,IAAI,UAAU,CAAC,CAC3B,KAAK,CAAE,KACR,CAEA,SAAS,qCAAQ,CAChB,UAAU,CAAE,IAAI,UAAU,CAAC,CAC3B,KAAK,CAAE,KAAK,CACZ,iBAAiB,CAAE,IAAI,SAAS,CACjC,CAEA,uCAAU,CACT,SAAS,CAAE,QACZ,CAEA,wCAAW,CACV,SAAS,CAAE,QACZ,CAEA,mCAAM,CACL,IAAI,CAAE,CAAC,CACP,UAAU,CAAE,MACb,CAEA,sCAAS,CACR,OAAO,CAAE,MAAM,CACf,SAAS,CAAE,MAAM,CACjB,MAAM,CAAE,CAAC,CAAC,IACX,CAEA,MAAO,YAAY,KAAK,CAAE,CACzB,sCAAS,CACR,KAAK,CAAE,IACR,CAEA,oBAAK,CAAC,iBAAE,CACR,wCAAW,CACV,OAAO,CAAE,IACV,CAEA,uCAAU,CACT,eAAe,CAAE,MAAM,CACvB,OAAO,CAAE,OACV,CAEA,sCAAS,CACR,OAAO,CAAE,IACV,CACD"}'
};
const Layout = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $page, $$unsubscribe_page;
  $$unsubscribe_page = subscribe(page, (value) => $page = value);
  const navItems = [
    {
      path: "/",
      label: "仪表盘",
      icon: "📊"
    },
    {
      path: "/properties",
      label: "房源管理",
      icon: "🏠"
    },
    {
      path: "/tenants",
      label: "租客管理",
      icon: "👤"
    },
    {
      path: "/contracts",
      label: "合同管理",
      icon: "📝"
    },
    {
      path: "/bills",
      label: "账单管理",
      icon: "💰"
    },
    {
      path: "/repairs",
      label: "维修报事",
      icon: "🔧"
    },
    {
      path: "/renewals",
      label: "续约管理",
      icon: "🔄"
    }
  ];
  let currentPath = "";
  function isActive(path) {
    if (path === "/") return currentPath === "/";
    return currentPath.startsWith(path);
  }
  $$result.css.add(css);
  currentPath = $page.url.pathname;
  $$unsubscribe_page();
  return `<div class="layout svelte-13bvrgb"><aside class="sidebar svelte-13bvrgb"><div class="logo svelte-13bvrgb" data-svelte-h="svelte-1sjum53"><span class="logo-icon svelte-13bvrgb">🏢</span> <h1 class="svelte-13bvrgb">房产管理系统</h1></div> <nav class="nav svelte-13bvrgb">${each(navItems, (item) => {
    return `<a${add_attribute("href", item.path, 0)} class="${["nav-item svelte-13bvrgb", isActive(item.path) ? "active" : ""].join(" ").trim()}"><span class="nav-icon svelte-13bvrgb">${escape(item.icon)}</span> <span class="nav-label svelte-13bvrgb">${escape(item.label)}</span> </a>`;
  })}</nav></aside> <main class="main svelte-13bvrgb"><div class="content svelte-13bvrgb">${slots.default ? slots.default({}) : ``}</div></main> </div>`;
});
export {
  Layout as default
};
