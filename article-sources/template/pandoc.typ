$definitions.typst()$

#let horizontalrule = line(length: 100%, stroke: 0.4pt + luma(180))

#let conf(
  title: "",
  authors: (),
  date: "",
  abstract: none,
  lang: "en",
  region: "US",
  font: (),
  fontsize: 9.5pt,
  sectionnumbering: none,
  pagenumbering: "1",
  cols: 1,
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm),
  paper: "a4",
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.5em,
  doc,
) = {
  let has-author = authors.len() > 0
  let author-str = if has-author { authors.first().name } else { [] }
  let has-date = date != ""

  set document(title: title)

  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
    number-align: center,
  )

  set text(
    font: ("Helvetica Neue", "Helvetica", "Nimbus Sans", "Liberation Sans"),
    size: fontsize,
    hyphenate: true,
    lang: lang,
  )

  set par(
    justify: true,
    leading: 0.65em,
    spacing: 0.9em,
  )

  show heading.where(level: 1): it => {
    set text(size: 13pt, weight: "bold")
    set block(above: 1.4em, below: 0.6em)
    it
  }

  show heading.where(level: 2): it => {
    set text(size: 10.5pt, weight: "bold")
    set block(above: 1.2em, below: 0.5em)
    it
  }

  show heading.where(level: 3): it => {
    set text(size: 9.5pt, weight: "bold", style: "italic")
    set block(above: 1em, below: 0.4em)
    it
  }

  show link: it => underline(stroke: 0.5pt, it)
  show footnote.entry: set text(size: 8pt)

  // ── Header ──────────────────────────────────────────────────────────────
  block(width: 100%, below: 0.4em)[
    #grid(
      columns: (1fr, auto),
      gutter: 0pt,
      align(left)[
        #text(size: 20pt, weight: "bold")[#title]
      ],
      align(right + bottom)[
        #text(size: 8.5pt, fill: luma(100))[
          #if has-author [#author-str]
          #if has-author and has-date [ · ]
          #if has-date [#date]
        ]
      ],
    )
  ]

  line(length: 100%, stroke: 0.6pt)
  v(0.6em)

  let has-abstract = abstract != none
  if has-abstract {
    block(width: 100%, below: 1.2em)[
      #set text(size: 9pt, style: "italic")
      #abstract
    ]
    line(length: 100%, stroke: 0.4pt + luma(180))
    v(0.8em)
  }

  // ── Two-column body ──────────────────────────────────────────────────────
  columns(2, gutter: 1.2em)[
    #doc
  ]
}

#show terms: it => {
  it.children
    .map(child => [
      #strong[#child.term]
      #block(inset: (left: 1.5em, top: -0.4em))[#child.description]
      ])
    .join()
}

#show: doc => conf(
$if(title)$  title: [$title$],
$endif$
$if(author)$  authors: (
$for(author)$
$if(author.name)$    ( name: [$author.name$], affiliation: [$author.affiliation$], email: [$author.email$] ),
$else$    ( name: [$author$], affiliation: [], email: [] ),
$endif$
$endfor$  ),
$endif$
$if(date)$  date: [$date$],
$endif$
$if(lang)$  lang: "$lang$",
$endif$
$if(abstract)$  abstract: [$abstract$],
$endif$
  doc,
)

$body$
