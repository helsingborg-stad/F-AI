<script module>
  import { defineMeta } from '@storybook/addon-svelte-csf'
  import Markdown from './Markdown.svelte'

  const source = `
# Header level 1

## Header level 2

### Header level 3

#### Header level 4

##### Header level 5

###### Header level 6

Paragraph

*Emphasis*

**Strong**

> Blockquote

1. Ordered List
2. Ordered List
3. Ordered List

- Unordered List
- Unordered List
- Unordered List

\`Inline Code\`

\`\`\`
Code Block => Hey
\`\`\`

Lorem ipsum dolor sit amet consectetur, adipisicing elit. Eius repellat illum maxime expedita! Voluptate rerum, facilis recusandae minus hic quibusdam porro architecto maxime dignissimos ratione eos natus ullam saepe amet!

Lorem ipsum dolor sit amet consectetur adipisicing elit. Aut, sed at nemo ipsum fugit nobis iusto harum reiciendis eius rerum molestias totam nesciunt corporis animi provident quia nostrum magni sit?
Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam perspiciatis minima voluptas nihil et consequatur vitae corrupti ipsam excepturi! Architecto sit recusandae debitis harum blanditiis. Alias nobis ab voluptate ex?

Lorem ipsum dolor sit amet **consectetur adipisicing elit**. Odio quisquam sed, suscipit, _accusantium cupiditate voluptatum deserunt_ in ad sapiente voluptate quasi quo blanditiis. _**Nemo excepturi perspiciatis illum, explicabo facere consectetur.**_

> Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex quaerat, et, non nam facere minima nulla tempora rerum nesciunt provident exercitationem, pariatur quas assumenda? Dolores vel id nesciunt obcaecati delectus.

> Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti quos provident ea, tempora quo, nostrum, illum libero dolores a ab facilis labore officiis? Ullam suscipit aliquam similique, odit quibusdam repellendus!
>
> > Lorem ipsum dolor sit amet, consectetur adipisicing elit. Suscipit quo corrupti, molestias consequatur quaerat similique autem quia repellendus soluta ullam cumque est eligendi delectus doloremque maxime. Necessitatibus commodi perspiciatis id?

1. First item
2. Second item
3. Three item
4. Four item

- First item
- Second item
- Three item
- Four item

Some code: \`export let myInt = 1;\`. Very good.

\`\`\`json
{
  "key": "some json value",
  "arr": [1, 2, 3]
}
\`\`\`

| Column A       | And B        |
| -------------- | ------------ |
| One value here | Another here |
| Row 2 Col 1    | Row 2 Col 2  |

Line below ⬇️

---

Line above ⬆️

Normal link: https://duckduckgo.com/

Named link: [DuckDuckGo](https://duckduckgo.com/)

\*\*\*\* Escaped character \*\*\*\*

~~Strikethrough~~

- [ ] Checklist A
- [x] Checklist B
- [ ] Checklist C

<p style="color: red;">Raw <span style="color: green; font-size: 1.5em;">HT</span>M<span style="color: cyan;">L</span> <span style="font-variant: small-caps; color: magenta;">TexT</span></p>

<!-- Image by Alessio Furlan https://unsplash.com/photos/a-snow-covered-mountain-range-under-a-cloudy-sky-4_Vii0UoMmI -->

![Cool Mountains](https://unsplash.com/photos/4_Vii0UoMmI/download?ixid=M3wxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNzI1ODc3MjYwfA&force=true&w=640)

<div id="raw-html-div" style="color: blue; background-color: cyan">

<!--Comment-->

# Raw HTML

<h1>Header 1</h1>
<span>Some span with <b>bold</b> and <i>italic</i> text.</span>
<button>Some button</button>

## Image

<img alt="scroll" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWFycm93LWJpZy1kb3duLWRhc2giPjxwYXRoIGQ9Ik0xNSA1SDkiLz48cGF0aCBkPSJNMTUgOXYzaDRsLTcgNy03LTdoNFY5eiIvPjwvc3ZnPg==" />
</div>

Peace ✌️
`

  const { Story } = defineMeta({
    title: 'Components/Markdown',
    tags: ['autodocs'],
  })
</script>

<Story name="Default" args={{ source }}>
  <Markdown {source} />
</Story>

<Story name="Prose style" args={{ source }}>
  <div class="prose prose-sm">
    <Markdown {source} />
  </div>
</Story>
