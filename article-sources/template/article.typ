// Article template — two-column layout, Helvetica
#let article(
  title: "",
  author: "",
  date: "",
  abstract: none,
  body,
) = {
  set document(title: title, author: author)

  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm),
    numbering: "1",
    number-align: center,
  )

  // Nimbus Sans is a metric-compatible Helvetica clone; Liberation Sans as fallback
  set text(
    font: ("Helvetica Neue", "Helvetica", "Nimbus Sans", "Liberation Sans"),
    size: 9.5pt,
    hyphenate: true,
    lang: "en",
  )

  set par(
    justify: true,
    leading: 0.65em,
    spacing: 0.9em,
  )

  // Headings
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

  // Links
  show link: it => underline(stroke: 0.5pt, it)

  // Footnotes
  show footnote.entry: set text(size: 8pt)

  // ── Header ──────────────────────────────────────────────────────────────
  block(width: 100%, below: 0.4em)[
    #set text(font: ("Helvetica Neue", "Helvetica", "Nimbus Sans", "Liberation Sans"))
    #grid(
      columns: (1fr, auto),
      gutter: 0pt,
      align(left)[
        #text(size: 20pt, weight: "bold")[#title]
      ],
      align(right + bottom)[
        #text(size: 8.5pt, fill: luma(100))[
          #if author != "" [#author]
          #if author != "" and date != "" [ · ]
          #if date != "" [#date]
        ]
      ],
    )
  ]

  line(length: 100%, stroke: 0.6pt)
  v(0.6em)

  // ── Abstract ────────────────────────────────────────────────────────────
  if abstract != none {
    block(width: 100%, below: 1.2em)[
      #set text(size: 9pt, style: "italic")
      #abstract
    ]
    line(length: 100%, stroke: 0.4pt + luma(180))
    v(0.8em)
  }

  // ── Two-column body ──────────────────────────────────────────────────────
  columns(2, gutter: 1.2em)[
    #body
  ]
}
