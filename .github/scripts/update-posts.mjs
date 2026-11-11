// Qiita の Atom フィードから最新 5 件を README に書き込む。
// 依存パッケージなし（Node 18 以降に入っている fetch だけを使う）。
//   本番: node .github/scripts/update-posts.mjs
//   確認: node .github/scripts/update-posts.mjs <保存した feed.xml>
import { readFileSync, writeFileSync } from 'node:fs';

const README = 'README.md';
const START = '<!-- posts:start -->';
const END = '<!-- posts:end -->';
const FEED = 'https://qiita.com/nemdull/feed';
// README に載せるのは自分の記事の URL だけ（フィードに想定外のリンクが混ざっても載せない）
const ALLOWED_LINK = /^https:\/\/qiita\.com\/nemdull\/items\/[0-9a-f]+$/;
const MAX_ITEMS = 5;

const decode = (s) =>
  s
    .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&');

const tagText = (xml, tag) => {
  const m = xml.match(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`));
  return m ? decode(m[1]).trim() : '';
};

const entryLink = (xml) => {
  const links = [...xml.matchAll(/<link\b([^>]*)\/?>/g)].map((m) => m[1]);
  const attr = (s, name) => (s.match(new RegExp(`\\b${name}\\s*=\\s*["']([^"']*)["']`)) || [])[1];
  const alt = links.find((l) => !attr(l, 'rel') || attr(l, 'rel') === 'alternate') ?? links[0];
  const href = alt ? decode(attr(alt, 'href') ?? '') : '';
  return href.split(/[?#]/)[0];
};

const entryDate = (xml) => {
  const raw = tagText(xml, 'updated') || tagText(xml, 'published');
  if (!raw) return '';
  const d = new Date(raw);
  return Number.isNaN(d.getTime()) ? raw.slice(0, 10) : d.toISOString().slice(0, 10);
};

// Markdown のリンク文字として安全な形にする（改行・角かっこ・HTML タグを無害化）
const safeTitle = (s) =>
  s
    .replace(/\s+/g, ' ')
    .replace(/\\/g, '\\\\')
    .replace(/\[/g, '\\[')
    .replace(/\]/g, '\\]')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .trim()
    .slice(0, 200);

const loadFeed = async () => {
  const local = process.argv[2];
  if (local) return readFileSync(local, 'utf8');
  const res = await fetch(FEED, { headers: { accept: 'application/atom+xml' } });
  if (!res.ok) throw new Error('Failed to fetch feed: ' + res.status);
  return res.text();
};

const xml = await loadFeed();
const items = [...xml.matchAll(/<entry\b[\s\S]*?<\/entry>/g)]
  .map((m) => m[0])
  .map((e) => ({ title: safeTitle(tagText(e, 'title')) || '(No title)', link: entryLink(e), date: entryDate(e) }))
  .filter((it) => ALLOWED_LINK.test(it.link))
  .slice(0, MAX_ITEMS)
  .map((it) => `- ${it.date} - [${it.title}](${it.link})`);

if (items.length === 0) {
  // フィードが空・形式が変わったときは README を消さずに、そのままにする
  console.log('No valid entries found. README left unchanged.');
  process.exit(0);
}

let md = readFileSync(README, 'utf8');
const block = `${START}\n${items.join('\n')}\n${END}`;
const re = new RegExp(`${START}[\\s\\S]*?${END}`, 'm');
md = re.test(md) ? md.replace(re, () => block) : `${md}\n\n${block}\n`;
writeFileSync(README, md);
console.log(`Updated ${items.length} posts.`);
