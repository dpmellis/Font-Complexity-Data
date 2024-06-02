# Font-Complexity-Data
DrawBot program for extracting data from fonts, plus sample data.

I wrote the program in DrawBot to extract glyph level data from fonts. Right now it just looks at the lower and uppercase letters in the English alphabet, but this can be easily changed. 

**IMPORTANT:** The number of on-curve (and total points) can't be meaningfully compared between TrueType and PostScript fonts. The former uses quadratic Bézier curves and the latter cubic. Because of the this TrueType outlines will always have a much larger number of points that PostScript outlines. 
See for instance
https://typo.social/@nicksherman/112405054308950066=

It creates a csv file with a row for every glyph with the following fields:

Font Name	— PostScript font name

Family	  — Name of the family

Serif     — Font Category

Weight	  — Weight, I use the description in the name, unless something else makes sene

Optical Size — Optical Size, I use text as a default

Italic     — Roman or Italic

Font Width — Width 

Style	     — Concatenation of Italic and Weight, useful for data analysis, could also concatenate Width and Optical Size

Case	     — Upper or lowercase

Glyph Name  

Glyph Width  — This includes the side bearings

Glyph Height — This should be 1000, but for some fonts it isn't, this variation
I don't think is significant

Shape Width	 — The width of just the glyph shape, no side bearings

Shape Height —	The height of just the glyph shape

Shape Area   — The area of a solid em square is 1

On Curve Points	— No duplicates

Total Points — Duplicates are allowed for offcurve points


**Sample row:**

Font Name	— ACaslonPro-Regular

Family	  — Adobe Caslon Pro

Serif     — Serif

Weight	  — Regular

Optical Size — Regular

Italic     — Roman

Font Width — Regular

Style	     — Roman Regular

Case	     — Upper

Glyph Name — A

Glyph Width — 743

Glyph Height — 1001

Shape Width	 — 744

Shape Height — 745

Shape Area	 — .124

On Curve Points	— 43

Total Points — 109
