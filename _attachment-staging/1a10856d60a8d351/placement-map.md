# Jill Lowe, "The daily grind - would you like pepper on that?" (Facts and Froth), for October 11, 2026

Source emails: `1a10852223945e2f` (article: PDF + Word via Mail Drop, to Judy and John) and
`1a10856d60a8d351` (12 photos, to John; "To be placed as in the article"). Jill, in the first email:
"There are 12 photos which are crucial to be in the position as submitted otherwise the article makes no sense."

Built Oct 4, 2026 from the PDF's own page geometry (`pdftohtml -xml`), with every embedded image matched to
its full-resolution file by image comparison (CLAUDE.md #68). All 12 matches are exact (difference 0.0 to
0.4; the next-best candidate is 36 or more). Nothing here is a guess.

**Use the PDF order.** The Word file lists photos 7 and 8 in the opposite order internally; the PDF is the
layout Jill refers to.

| # | File (full-resolution name) | Pixels | PDF page | Position | Caption in the PDF |
|---|---|---|---|---|---|
| 1 | `shutterstock_2287821993.jpg` | 8192x5464 | 1 | After the opening paragraph "Who knew that this unassuming dried fruit…" | none |
| 2 | `shutterstock_1779694760.jpg` | 2967x1844 | 2 | After "And oh yes! it is the piperine which can trigger a sneeze!" | "The Piper Nigrum (black peppercorn) on the flowering climbing vine" (italic) |
| 3 | `IMG_2855.jpeg` | 1030x744 | 3 | Top of page 3, before "Not only do we take black pepper for granted…" | none |
| 4 | `shutterstock_2746066031.jpg` | 6720x4480 | 3 | After the "Not only do we take black pepper for granted…" paragraph | none |
| 5 | `IMG_2782.jpeg` | 1206x1781 | 4 | After "He interviewed Sebastion Prange…" (end of the "How did pepper find its way to our dinner tables?" section on that page) | none |
| 6 | `shutterstock_1714067527.jpg` | 7360x4912 | 5 | After "As the unknown 'East' became known and ownable…" | none |
| 7 | `shutterstock_2624028293.jpg` | 5184x3456 | 6 | Top of page 6, before the heading "How to taste-test pepper" | none |
| 8 | `IMG_2867.jpeg` | 1066x799 | 6 | After the "Whether you choose varieties of pepper…" paragraph | none |
| 9 | `Image 3.jpg` | 750x500 | 7 | After the "The Pepper Grinder" paragraph ("The bland, pre-ground pepper…") | none |
| 10 | `IMG_2577.jpeg` | 1206x1281 | 8 | After "The Dish : Filet de bœuf au poivre de Sarawak…"; followed by the line "18 Rue Paul Bert 65011 Paris." | none (the address line follows it) |
| 11 | `IMG_2579.jpeg` | 1201x1719 | 9 | Full page 9, alone | none |
| 12 | `IMG_2574.jpeg` | 1180x1273 | 10 | After "Couldn't you pop over to Paris to Le Bistrot Paul Bert…"; before "A sober footnote." | none |

Notes for the build:

- Column name "Facts and Froth"; byline Jill Lowe; title as above. Section headings in the PDF: "How did pepper
  find its way to our dinner tables?", "How to taste-test pepper", "The Pepper Grinder", "The 'Steak au Poivre'".
- The PDF has bold and italic runs throughout (for example *piperine*, *Ayurvedic medicine*, *Every Bite*,
  *Monsoon Islam : Trade and Faith on the Medieval Malabar Coast*, *Guild of Pepperers*, *Le Bistrot Paul Bert*,
  and the closing "A sober footnote." paragraph). Take them from the rendered pages, not from plain text (#43).
- No hyperlinks in the PDF or the Word file.
- The Word file keeps its text in boxes; python-docx sees the 12 images but no paragraphs. Work from the PDF.
- `full-resolution/` holds web-size copies (longest side 3000 px) of the 12 originals, under their original
  names. The originals are in Jill's Mail Drop `Images.zip` (60 MB, link valid until Nov 3, 2026). The 12 files
  beside this note are the 320 to 640 px previews Mail attached; do not use them.
- Five originals are stock photos (Shutterstock filenames). No credits were supplied.
